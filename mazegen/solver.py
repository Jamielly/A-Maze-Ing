"""Module responsible for solving the maze and finding the shortest path using Breadth-First Search."""

from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen.cell import Cell


class MazeSolver:
    """Calculates the shortest path through the maze using Breadth-First Search (BFS)."""

    def __init__(
        self, grid: list[list["Cell"]], width: int, height: int
    ) -> None:
        """Initializes the maze solver with the maze grid and dimensions.

        Args:
            grid: The 2D grid matrix of cells representing the maze.
            width: Width of the maze (number of columns).
            height: Height of the maze (number of rows).
        """
        self.grid: list[list["Cell"]] = grid
        self.width: int = width
        self.height: int = height

    def find_shortest_path(
        self, start: tuple[int, int], end: tuple[int, int]
    ) -> tuple[list[tuple[int, int]], str]:
        """Calculates the shortest path from start to end coordinates using BFS.

        Args:
            start: (x, y) coordinates of the starting point.
            end: (x, y) coordinates of the ending/exit point.

        Returns:
            A tuple containing a list of coordinate tuples for the path and a string of direction characters.
        """
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
