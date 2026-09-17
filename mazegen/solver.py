from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen.cell import Cell


class MazeSolver:
    def __init__(
        self, grid: list[list["Cell"]], width: int, height: int
    ) -> None:
        self.grid: list[list["Cell"]] = grid
        self.width: int = width
        self.height: int = height

    def find_shortest_path(
        self, start: tuple[int, int], end: tuple[int, int]
    ) -> tuple[list[tuple[int, int]], str]:
        queue: deque[tuple[int, int]] = deque([start])
        parent: dict[tuple[int, int], tuple[tuple[int, int], str] | None] = {
            start: None
        }
        directions = [
            (1, 0, -1, "N"),
            (2, 1, 0, "E"),
            (4, 0, 1, "S"),
            (8, -1, 0, "W"),
        ]

        found = False
        while queue:
            curr = queue.popleft()
            if curr == end:
                found = True
                break

            cx, cy = curr
            curr_cell = self.grid[cy][cx]

            for wall_bit, dx, dy, dir_char in directions:
                if not curr_cell.has_wall(wall_bit):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        neighbor = (nx, ny)
                        if neighbor not in parent:
                            parent[neighbor] = (curr, dir_char)
                            queue.append(neighbor)

        if not found:
            return ([], "")

        path_coords: list[tuple[int, int]] = []
        path_chars: list[str] = []
        curr_step: tuple[int, int] | None = end

        while curr_step is not None:
            path_coords.append(curr_step)
            step_info = parent[curr_step]
            if step_info is not None:
                prev_coord, dir_char = step_info
                path_chars.append(dir_char)
                curr_step = prev_coord
            else:
                curr_step = None

        path_coords.reverse()
        path_chars.reverse()

        return path_coords, "".join(path_chars)
