```python
"""Generator module for creating perfect and playable mazes."""

import random
from typing import Callable

from mazegen.cell import Cell
from mazegen.solver import MazeSolver


# Callback chamado durante a geração:
# (grid_atual, coordenada_atual)
StepCallback = Callable[[list[list[Cell]], tuple[int, int]], None]


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

        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError("Entry position is outside the maze.")

        if not (0 <= exit_pos[0] < width and 0 <= exit_pos[1] < height):
            raise ValueError("Exit position is outside the maze.")

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_pos
        self.perfect = perfect
        self.seed = seed

        self.grid: list[list[Cell]] = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]

        self._randomizer = random.Random(seed)

    def generate(
        self,
        step_callback: StepCallback | None = None,
    ) -> list[list[Cell]]:
        """
        Generate the complete maze.

        If ``step_callback`` is provided, it is called during the
        generation process with:

            (current_grid, current_position)

        This can be used by a graphical interface to animate the
        maze generation.
        """

        # Reset the random generator when a seed was provided.
        if self.seed is not None:
            self._randomizer.seed(self.seed)

        # Reserve the "42" pattern.
        self._embed_pattern_42()

        # Generate the maze using DFS / Recursive Backtracking.
        self._carve_perfect_maze(step_callback)

        # In playable mode, add extra connections.
        if not self.perfect:
            self._carve_playable_loops()

        # Make sure neighboring cells have matching walls.
        self._enforce_wall_consistency()

        # Final callback so the renderer receives the completed maze.
        if step_callback:
            step_callback(self.grid, self.entry)

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

        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        if (
            self.width < pattern_width + 4
            or self.height < pattern_height + 4
        ):
            return False

        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        for row, pattern_row in enumerate(pattern):
            for col, char in enumerate(pattern_row):

                if char != "X":
                    continue

                grid_x = start_x + col
                grid_y = start_y + row

                cell = self.grid[grid_y][grid_x]

                cell.is_pattern_42 = True
                cell.visited = True
                cell.walls = 15

        return True

    def _carve_perfect_maze(
        self,
        step_callback: StepCallback | None = None,
    ) -> None:
        """
        Generate a maze using DFS / Recursive Backtracking.

        The algorithm keeps a stack of cells and randomly chooses
        unvisited neighbors. When no unvisited neighbor exists,
        it backtracks.
        """

        start_x, start_y = self.entry

        # If the entry happens to be inside the 42 pattern,
        # use the first available cell instead.
        if self.grid[start_y][start_x].is_pattern_42:
            start_x, start_y = self._find_valid_start()

        stack: list[tuple[int, int]] = [(start_x, start_y)]

        self.grid[start_y][start_x].visited = True

        directions = [
            (Cell.NORTH, 0, -1, Cell.SOUTH),
            (Cell.EAST, 1, 0, Cell.WEST),
            (Cell.SOUTH, 0, 1, Cell.NORTH),
            (Cell.WEST, -1, 0, Cell.EAST),
        ]

        while stack:
            current_x, current_y = stack[-1]

            # Notify the renderer about the current position.
            if step_callback:
                step_callback(
                    self.grid,
                    (current_x, current_y),
                )

            unvisited_neighbors: list[
                tuple[int, int, int, int]
            ] = []

            for wall_bit, dx, dy, opposite_bit in directions:

                next_x = current_x + dx
                next_y = current_y + dy

                if not (
                    0 <= next_x < self.width
                    and 0 <= next_y < self.height
                ):
                    continue

                neighbor = self.grid[next_y][next_x]

                if neighbor.visited:
                    continue

                if neighbor.is_pattern_42:
                    continue

                unvisited_neighbors.append(
                    (
                        wall_bit,
                        dx,
                        dy,
                        opposite_bit,
                    )
                )

            if unvisited_neighbors:

                wall_bit, dx, dy, opposite_bit = (
                    self._randomizer.choice(
                        unvisited_neighbors
                    )
                )

                next_x = current_x + dx
                next_y = current_y + dy

                # Remove the wall between the current cell
                # and the selected neighbor.
                self.grid[current_y][current_x].set_wall(
                    wall_bit,
                    False,
                )

                self.grid[next_y][next_x].set_wall(
                    opposite_bit,
                    False,
                )

                self.grid[next_y][next_x].visited = True

                stack.append((next_x, next_y))

            else:
                # No unvisited neighbors -> backtrack.
                stack.pop()

    def _find_valid_start(self) -> tuple[int, int]:
        """Find the first cell that is not part of the 42 pattern."""

        for y in range(self.height):
            for x in range(self.width):

                if not self.grid[y][x].is_pattern_42:
                    return x, y

        raise ValueError(
            "The maze does not contain any available cells."
        )

    def _has_3x3_open(self) -> bool:
        """
        Check whether there is a completely open 3x3 area.

        This prevents the playable maze from developing excessively
        large open spaces.
        """

        if self.width < 3 or self.height < 3:
            return False

        for y in range(self.height - 2):
            for x in range(self.width - 2):

                open_area = True

                for row in range(3):
                    for col in range(3):

                        cell = self.grid[y + row][x + col]

                        # Check horizontal connections.
                        if col < 2 and cell.has_wall(Cell.EAST):
                            open_area = False
                            break

                        # Check vertical connections.
                        if row < 2 and cell.has_wall(Cell.SOUTH):
                            open_area = False
                            break

                    if not open_area:
                        break

                if open_area:
                    return True

        return False

    def _carve_playable_loops(self) -> None:
        """
        Open additional routes for Pac-Man style gameplay.

        The extra connections create loops while avoiding excessively
        large 3x3 completely open areas.
        """

        corners = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]

        center = (
            self.width // 2,
            self.height // 2,
        )

        special_positions = corners + [center]

        loop_directions = [
            (
                Cell.EAST,
                1,
                0,
                Cell.WEST,
            ),
            (
                Cell.SOUTH,
                0,
                1,
                Cell.NORTH,
            ),
        ]

        # First create a few deterministic connections around
        # corners and center.
        for current_x, current_y in special_positions:

            if not (
                0 <= current_x < self.width
                and 0 <= current_y < self.height
            ):
                continue

            current_cell = self.grid[current_y][current_x]

            if current_cell.is_pattern_42:
                continue

            for wall_bit, dx, dy, opposite_bit in loop_directions:

                next_x = current_x + dx
                next_y = current_y + dy

                if not (
                    0 <= next_x < self.width
                    and 0 <= next_y < self.height
                ):
                    continue

                next_cell = self.grid[next_y][next_x]

                if next_cell.is_pattern_42:
                    continue

                current_cell.set_wall(
                    wall_bit,
                    False,
                )

                next_cell.set_wall(
                    opposite_bit,
                    False,
                )

        # Find additional walls that can potentially be removed.
        candidate_walls: list[
            tuple[int, int, int, int, int, int]
        ] = []

        for y in range(self.height):
            for x in range(self.width):

                current_cell = self.grid[y][x]

                if current_cell.is_pattern_42:
                    continue

                # East wall.
                if x + 1 < self.width:

                    next_cell = self.grid[y][x + 1]

                    if (
                        not next_cell.is_pattern_42
                        and current_cell.has_wall(Cell.EAST)
                    ):
                        candidate_walls.append(
                            (
                                x,
                                y,
                                Cell.EAST,
                                x + 1,
                                y,
                                Cell.WEST,
                            )
                        )

                # South wall.
                if y + 1 < self.height:

                    next_cell = self.grid[y + 1][x]

                    if (
                        not next_cell.is_pattern_42
                        and current_cell.has_wall(Cell.SOUTH)
                    ):
                        candidate_walls.append(
                            (
                                x,
                                y,
                                Cell.SOUTH,
                                x,
                                y + 1,
                                Cell.NORTH,
                            )
                        )

        self._randomizer.shuffle(candidate_walls)

        target_loops = max(
            2,
            (self.width * self.height) // 20,
        )

        loops_added = 0

        for (
            x,
            y,
            wall_bit,
            next_x,
            next_y,
            opposite_bit,
        ) in candidate_walls:

            if loops_added >= target_loops:
                break

            current_cell = self.grid[y][x]
            next_cell = self.grid[next_y][next_x]

            # Temporarily remove the wall.
            current_cell.set_wall(
                wall_bit,
                False,
            )

            next_cell.set_wall(
                opposite_bit,
                False,
            )

            # Reject the change if it creates a large open area.
            if self._has_3x3_open():

                current_cell.set_wall(
                    wall_bit,
                    True,
                )

                next_cell.set_wall(
                    opposite_bit,
                    True,
                )

            else:
                loops_added += 1

    def _enforce_wall_consistency(self) -> None:
        """
        Ensure shared walls between neighboring cells are identical.
        """

        for y in range(self.height):
            for x in range(self.width):

                cell = self.grid[y][x]

                # East / West consistency.
                if x + 1 < self.width:

                    east_neighbor = self.grid[y][x + 1]

                    has_east_wall = cell.has_wall(Cell.EAST)

                    east_neighbor.set_wall(
                        Cell.WEST,
                        has_east_wall,
                    )

                # South / North consistency.
                if y + 1 < self.height:

                    south_neighbor = self.grid[y + 1][x]

                    has_south_wall = cell.has_wall(Cell.SOUTH)

                    south_neighbor.set_wall(
                        Cell.NORTH,
                        has_south_wall,
                    )

    def get_solution(
        self,
    ) -> tuple[list[tuple[int, int]], str]:
        """Return the shortest path coordinates and direction string."""

        solver = MazeSolver(
            self.grid,
            self.width,
            self.height,
        )

        return solver.find_shortest_path(
            self.entry,
            self.exit,
        )
```