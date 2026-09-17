import random
from typing import Callable

from mazegen.cell import Cell
from mazegen.solver import MazeSolver


StepCallback = Callable[
    [list[list[Cell]], tuple[int, int]],
    None,
]


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int] = (0, 0),
        exit_pos: tuple[int, int] = (0, 0),
        perfect: bool = False,
        seed: int | None = None,
    ) -> None:
        if width <= 0 or height <= 0:
            raise ValueError(
            )

        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError("Entry position is outside the maze.")

        if not (
            0 <= exit_pos[0] < width
            and 0 <= exit_pos[1] < height
        ):
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
        if self.seed is not None:
            self._randomizer.seed(self.seed)

        self._embed_pattern_42()
        self._carve_perfect_maze(step_callback)

        if not self.perfect:
            self._carve_playable_loops()

        self._enforce_wall_consistency()

        if step_callback:
            step_callback(self.grid, self.entry)

        return self.grid

    def _embed_pattern_42(self) -> bool:
        pattern = [
            "X X XXX",
            "X X   X",
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

        center = (self.width // 2, self.height // 2)
        start_x = center[0] - (pattern_width // 2)
        start_y = center[1] - (pattern_height // 2)

        for row, pattern_row in enumerate(pattern):
            for col, char in enumerate(pattern_row):
                if char != "X":
                    continue

                x = start_x + col
                y = start_y + row

                if (x, y) in (self.entry, self.exit, center):
                    continue

                cell = self.grid[y][x]
                cell.is_pattern_42 = True
                cell.visited = True
                cell.walls = 15

        return True

    def _carve_perfect_maze(
        self,
        step_callback: StepCallback | None = None,
    ) -> None:
        """Generate the maze using iterative DFS backtracking."""

        start_x, start_y = self.entry

        if self.grid[start_y][start_x].is_pattern_42:
            start_x, start_y = self._find_valid_start()

        stack: list[tuple[int, int]] = [
            (start_x, start_y)
        ]

        self.grid[start_y][start_x].visited = True

        if step_callback:
            step_callback(self.grid, (start_x, start_y))

        directions = [
            (Cell.NORTH, 0, -1, Cell.SOUTH),
            (Cell.EAST, 1, 0, Cell.WEST),
            (Cell.SOUTH, 0, 1, Cell.NORTH),
            (Cell.WEST, -1, 0, Cell.EAST),
        ]

        while stack:
            current_x, current_y = stack[-1]

            neighbors: list[
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

                neighbors.append(
                    (
                        wall_bit,
                        dx,
                        dy,
                        opposite_bit,
                    )
                )

            if not neighbors:
                stack.pop()
                continue

            wall_bit, dx, dy, opposite_bit = (
                self._randomizer.choice(neighbors)
            )

            next_x = current_x + dx
            next_y = current_y + dy

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

            if step_callback:
                step_callback(
                    self.grid,
                    (next_x, next_y),
                )

    def _find_valid_start(self) -> tuple[int, int]:
        for y in range(self.height):
            for x in range(self.width):
                if not self.grid[y][x].is_pattern_42:
                    return x, y

        raise ValueError(
        )

    def _has_3x3_open(self) -> bool:
        if self.width < 3 or self.height < 3:
            return False

        for y in range(self.height - 2):
            for x in range(self.width - 2):
                open_area = True

                for row in range(3):
                    for col in range(3):
                        cell = self.grid[y + row][x + col]

                        if col < 2 and cell.has_wall(Cell.EAST):
                            open_area = False
                            break

                        if row < 2 and cell.has_wall(Cell.SOUTH):
                            open_area = False
                            break

                    if not open_area:
                        break

                if open_area:
                    return True

        return False

    def _carve_playable_loops(self) -> None:
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

        directions = [
            (Cell.EAST, 1, 0, Cell.WEST),
            (Cell.SOUTH, 0, 1, Cell.NORTH),
        ]

        for x, y in special_positions:
            if self.grid[y][x].is_pattern_42:
                continue

            for wall_bit, dx, dy, opposite_bit in directions:
                nx = x + dx
                ny = y + dy

                if not (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                ):
                    continue

                if self.grid[ny][nx].is_pattern_42:
                    continue

                self.grid[y][x].set_wall(
                    wall_bit,
                    False,
                )

                self.grid[ny][nx].set_wall(
                    opposite_bit,
                    False,
                )

        candidate_walls: list[
            tuple[int, int, int, int, int, int]
        ] = []

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                if cell.is_pattern_42:
                    continue

                if x + 1 < self.width:
                    neighbor = self.grid[y][x + 1]

                    if (
                        not neighbor.is_pattern_42
                        and cell.has_wall(Cell.EAST)
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

                if y + 1 < self.height:
                    neighbor = self.grid[y + 1][x]

                    if (
                        not neighbor.is_pattern_42
                        and cell.has_wall(Cell.SOUTH)
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
            nx,
            ny,
            opposite_bit,
        ) in candidate_walls:

            if loops_added >= target_loops:
                break

            cell = self.grid[y][x]
            neighbor = self.grid[ny][nx]

            cell.set_wall(wall_bit, False)
            neighbor.set_wall(opposite_bit, False)

            if self._has_3x3_open():
                cell.set_wall(wall_bit, True)
                neighbor.set_wall(opposite_bit, True)
            else:
                loops_added += 1

        self._braid_dead_ends()

    def _braid_dead_ends(self) -> None:
        all_dirs = [
            (Cell.NORTH, 0, -1, Cell.SOUTH),
            (Cell.EAST, 1, 0, Cell.WEST),
            (Cell.SOUTH, 0, 1, Cell.NORTH),
            (Cell.WEST, -1, 0, Cell.EAST),
        ]

        changed = True
        while changed:
            changed = False
            dead_ends: list[tuple[int, int]] = []
            for y in range(self.height):
                for x in range(self.width):
                    cell = self.grid[y][x]
                    if cell.is_pattern_42:
                        continue
                    wall_count = bin(cell.walls).count("1")
                    if wall_count >= 3:
                        dead_ends.append((x, y))

            self._randomizer.shuffle(dead_ends)
            for x, y in dead_ends:
                cell = self.grid[y][x]
                if bin(cell.walls).count("1") < 3:
                    continue

                candidates: list[tuple[int, int, int, int]] = []
                for w_bit, dx, dy, opp_bit in all_dirs:
                    if cell.has_wall(w_bit):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            neighbor = self.grid[ny][nx]
                            if not neighbor.is_pattern_42:
                                candidates.append((w_bit, nx, ny, opp_bit))

                self._randomizer.shuffle(candidates)
                for w_bit, nx, ny, opp_bit in candidates:
                    neighbor = self.grid[ny][nx]
                    cell.set_wall(w_bit, False)
                    neighbor.set_wall(opp_bit, False)
                    if self._has_3x3_open():
                        cell.set_wall(w_bit, True)
                        neighbor.set_wall(opp_bit, True)
                    else:
                        changed = True
                        break

    def _enforce_wall_consistency(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                if x + 1 < self.width:
                    neighbor = self.grid[y][x + 1]
                    has_wall = cell.has_wall(Cell.EAST)

                    neighbor.set_wall(
                        Cell.WEST,
                        has_wall,
                    )

                if y + 1 < self.height:
                    neighbor = self.grid[y + 1][x]
                    has_wall = cell.has_wall(Cell.SOUTH)

                    neighbor.set_wall(
                        Cell.NORTH,
                        has_wall,
                    )

    def get_solution(
        self,
    ) -> tuple[list[tuple[int, int]], str]:
        solver = MazeSolver(
            self.grid,
            self.width,
            self.height,
        )

        return solver.find_shortest_path(
            self.entry,
            self.exit,
        )
