"""Renderer module for ASCII maze terminal display with ANSI colors."""

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen.cell import Cell


class TerminalRenderer:
    """Render the maze and interactive menu using ANSI colors."""

    def __init__(self) -> None:
        """Initialize renderer options and ANSI color palettes."""
        self.show_path: bool = True
        self.color_index: int = 0
        self.palettes: list[str] = [
            "\033[32m",  # Green
            "\033[33m",  # Yellow
            "\033[36m",  # Cyan
            "\033[35m",  # Magenta
        ]
        self._reset: str = "\033[0m"

    def toggle_path(self) -> None:
        """Toggle the shortest path display on or off."""
        self.show_path = not self.show_path

    def rotate_colors(self) -> None:
        """Cycle to the next wall color palette."""
        self.color_index = (self.color_index + 1) % len(self.palettes)

    def render_generation(
        self,
        grid: list[list["Cell"]],
        head: tuple[int, int],
    ) -> None:
        """Render a single animation frame during maze generation."""
        height = len(grid)
        if height == 0:
            return

        width = len(grid[0])
        if width == 0:
            return

        wall_color = self.palettes[self.color_index]
        print("\033[H", end="")

        buf_h = 2 * height + 1
        buf_w = 2 * width + 1
        buffer: list[list[str]] = [
            [" " for _ in range(buf_w)] for _ in range(buf_h)
        ]

        for r_idx in range(0, buf_h, 2):
            for c_idx in range(0, buf_w, 2):
                buffer[r_idx][c_idx] = "█"

        for y in range(height):
            for x in range(width):
                cell = grid[y][x]
                cy = 2 * y + 1
                cx = 2 * x + 1

                if cell.has_wall(1):
                    buffer[cy - 1][cx] = "█"
                if cell.has_wall(2):
                    buffer[cy][cx + 1] = "█"
                if cell.has_wall(4):
                    buffer[cy + 1][cx] = "█"
                if cell.has_wall(8):
                    buffer[cy][cx - 1] = "█"

                coord = (x, y)
                if coord == head:
                    buffer[cy][cx] = "\033[93m●\033[0m"
                elif cell.is_pattern_42:
                    buffer[cy][cx] = "\033[90m█\033[0m"

        print("=== A-Maze-ing ===")
        for grid_row in buffer:
            line = "".join(
                f"{wall_color}█{self._reset}" if char == "█" else char
                for char in grid_row
            )
            print(line)

        print()
        print("Generating maze...")

    def render(
        self,
        grid: list[list["Cell"]],
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        path: list[tuple[int, int]],
    ) -> None:
        """Print the complete ASCII maze and menu options in terminal."""
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0

        if width == 0 or height == 0:
            print("Empty maze grid.")
            return

        wall_color = self.palettes[self.color_index]
        path_set = set(path) if (self.show_path and path) else set()

        os.system("clear" if os.name == "posix" else "cls")

        buf_h = 2 * height + 1
        buf_w = 2 * width + 1
        buffer: list[list[str]] = [
            [" " for _ in range(buf_w)] for _ in range(buf_h)
        ]

        for r_idx in range(0, buf_h, 2):
            for c_idx in range(0, buf_w, 2):
                buffer[r_idx][c_idx] = "█"

        for y in range(height):
            for x in range(width):
                cell = grid[y][x]
                cy = 2 * y + 1
                cx = 2 * x + 1

                if cell.has_wall(1):
                    buffer[cy - 1][cx] = "█"
                if cell.has_wall(2):
                    buffer[cy][cx + 1] = "█"
                if cell.has_wall(4):
                    buffer[cy + 1][cx] = "█"
                if cell.has_wall(8):
                    buffer[cy][cx - 1] = "█"

                coord = (x, y)
                if coord == entry:
                    buffer[cy][cx] = "\033[95mE\033[0m"
                elif coord == exit_pos:
                    buffer[cy][cx] = "\033[91mX\033[0m"
                elif cell.is_pattern_42:
                    buffer[cy][cx] = "\033[90m█\033[0m"
                elif coord in path_set:
                    buffer[cy][cx] = "\033[94m•\033[0m"

        print("=== A-Maze-ing ===")
        for grid_row in buffer:
            line = "".join(
                f"{wall_color}█{self._reset}" if char == "█" else char
                for char in grid_row
            )
            print(line)

        path_status = "ON" if self.show_path else "OFF"
        print(f"\nPath display: {path_status}")
        print("Menu:")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
