"""Generator module for creating perfect and playable mazes."""

import random
from typing import TYPE_CHECKING

from mazegen.cell import Cell
from mazegen.solver import MazeSolver


class MazeGenerator:
    """Generates perfect or Pac-Man playable mazes with a 42 pattern."""

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int] = (0, 0),
        exit_pos: tuple[int, int] = (0, 0),
        perfect: bool = False,
        seed: int | None = None,
    ) -> None:
        """Initialize the maze generator with grid dimensions and options."""
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive integers.")

        self.width: int = width
        self.height: int = height
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit_pos
        self.perfect: bool = perfect
        self.seed: int | None = seed

        self.grid: list[list[Cell]] = [
            [Cell(x, y) for x in range(width)] for y in range(height)
        ]
        self._randomizer: random.Random = random.Random(seed)

    def generate(self) -> list[list[Cell]]:
        """Generate the complete maze grid based on settings."""
        if self.seed is not None:
            self._randomizer.seed(self.seed)

        self._embed_pattern_42()
        self._carve_perfect_maze()

        if not self.perfect:
            self._carve_playable_loops()

        self._enforce_wall_consistency()
        return self.grid

    def _embed_pattern_42(self) -> bool:
        """Draw the '42' pattern in closed cells at the center of the grid."""
        pattern = [
            "X   XXX",
            "X     X",
            "XXX XXX",
            "  X X  ",
            "  X XXX",
        ]
        pat_h = len(pattern)
        pat_w = len(pattern[0])

        if self.width < 11 or self.height < 9:
            print("Warning: Grid too small to embed '42' pattern.")
            return False

        start_x = (self.width - pat_w) // 2
        start_y = (self.height - pat_h) // 2

        for r, row in enumerate(pattern):
            for c, char in enumerate(row):
                if char == "X":
                    gx = start_x + c
                    gy = start_y + r
                    cell = self.grid[gy][gx]
                    cell.is_pattern_42 = True
                    cell.visited = True
                    cell.walls = 15

        return True

    def _carve_perfect_maze(self) -> None:
        """Carve a perfect maze using the Recursive Backtracking algorithm."""
        start_x, start_y = self.entry
        if self.grid[start_y][start_x].is_pattern_42:
            start_x, start_y = 0, 0

        stack: list[tuple[int, int]] = [(start_x, start_y)]
        self.grid[start_y][start_x].visited = True

        directions = [
            (Cell.NORTH, 0, -1, Cell.SOUTH),
            (Cell.EAST, 1, 0, Cell.WEST),
            (Cell.SOUTH, 0, 1, Cell.NORTH),
            (Cell.WEST, -1, 0, Cell.EAST),
        ]

        while stack:
            cx, cy = stack[-1]
            unvisited_neighbors: list[tuple[int, int, int, int]] = []

            for wall_bit, dx, dy, opp_bit in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbor = self.grid[ny][nx]
                    if not neighbor.visited and not neighbor.is_pattern_42:
                        unvisited_neighbors.append((wall_bit, dx, dy, opp_bit))

            if unvisited_neighbors:
                w_bit, dx, dy, opp_bit = self._randomizer.choice(
                    unvisited_neighbors
                )
                nx, ny = cx + dx, cy + dy

                self.grid[cy][cx].set_wall(w_bit, False)
                self.grid[ny][nx].set_wall(opp_bit, False)
                self.grid[ny][nx].visited = True

                stack.append((nx, ny))
            else:
                stack.pop()

    def _has_3x3_open(self) -> bool:
        """Check if any 3x3 area is completely devoid of walls."""
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                open_area = True
                for r in range(3):
                    for c in range(3):
                        cell = self.grid[y + r][x + c]
                        if c < 2 and cell.has_wall(Cell.EAST):
                            open_area = False
                            break
                        if r < 2 and cell.has_wall(Cell.SOUTH):
                            open_area = False
                            break
                    if not open_area:
                        break
                if open_area:
                    return True
        return False

    def _carve_playable_loops(self) -> None:
        """Open extra routes and loops for Pac-Man playable mode."""
        corners = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]
        center = (self.width // 2, self.height // 2)

        for cx, cy in corners + [center]:
            for wall_bit, dx, dy, opp_bit in [
                (Cell.EAST, 1, 0, Cell.WEST),
                (Cell.SOUTH, 0, 1, Cell.NORTH),
            ]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (
                        not self.grid[cy][cx].is_pattern_42
                        and not self.grid[ny][nx].is_pattern_42
                    ):
                        self.grid[cy][cx].set_wall(wall_bit, False)
                        self.grid[ny][nx].set_wall(opp_bit, False)

        candidate_walls: list[tuple[int, int, int, int, int, int]] = []
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].is_pattern_42:
                    continue
                if x + 1 < self.width and not self.grid[y][x + 1].is_pattern_42:
                    if self.grid[y][x].has_wall(Cell.EAST):
                        candidate_walls.append(
                            (x, y, Cell.EAST, x + 1, y, Cell.WEST)
                        )
                if y + 1 < self.height and not self.grid[y + 1][x].is_pattern_42:
                    if self.grid[y][x].has_wall(Cell.SOUTH):
                        candidate_walls.append(
                            (x, y, Cell.SOUTH, x, y + 1, Cell.NORTH)
                        )

        self._randomizer.shuffle(candidate_walls)
        target_loops = max(2, (self.width * self.height) // 20)
        loops_added = 0

        for x, y, w_bit, nx, ny, opp_bit in candidate_walls:
            if loops_added >= target_loops:
                break
            self.grid[y][x].set_wall(w_bit, False)
            self.grid[ny][nx].set_wall(opp_bit, False)

            if self._has_3x3_open():
                self.grid[y][x].set_wall(w_bit, True)
                self.grid[ny][nx].set_wall(opp_bit, True)
            else:
                loops_added += 1

    def _enforce_wall_consistency(self) -> None:
        """Ensure shared walls between neighboring cells are identical."""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if x + 1 < self.width:
                    east_neighbor = self.grid[y][x + 1]
                    has_east = cell.has_wall(Cell.EAST)
                    east_neighbor.set_wall(Cell.WEST, has_east)
                if y + 1 < self.height:
                    south_neighbor = self.grid[y + 1][x]
                    has_south = cell.has_wall(Cell.SOUTH)
                    south_neighbor.set_wall(Cell.NORTH, has_south)

    def get_solution(self) -> tuple[list[tuple[int, int]], str]:
        """Return the shortest path coordinates and direction string."""

        solver = MazeSolver(self.grid, self.width, self.height)
        return solver.find_shortest_path(self.entry, self.exit)
