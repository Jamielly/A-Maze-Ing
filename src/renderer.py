"""Renderer module for ASCII maze terminal display with ANSI colors."""

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen.cell import Cell


class TerminalRenderer:
    """Render the maze and interactive
    menu in the terminal using ANSI colors."""

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

    def render(
        self,
        grid: list[list["Cell"]],
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        path: list[tuple[int, int]],
    ) -> None:
        """Print the ASCII maze and menu options in the terminal."""
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0

        if width == 0 or height == 0:
            print("Empty maze grid.")
            return

        wall_color = self.palettes[self.color_index]
        path_set = set(path) if (self.show_path and path) else set()

        # Clear terminal screen
        os.system("clear" if os.name == "posix" else "cls")

        # 2D character buffer: (2*height + 1) rows x (2*width + 1) cols
        buf_h = 2 * height + 1
        buf_w = 2 * width + 1
        buffer: list[list[str]] = [[" " for _ in range(buf_w)] for _ in range(buf_h)]

        # Fill default wall intersections/corners
        for r in range(0, buf_h, 2):
            for c in range(0, buf_w, 2):
                buffer[r][c] = "█"

        # Populate cell walls and centers
        for y in range(height):
            for x in range(width):
                cell = grid[y][x]
                cy, cx = 2 * y + 1, 2 * x + 1

                # North wall (bit 1)
                if cell.has_wall(1):
                    buffer[cy - 1][cx] = "█"
                # East wall (bit 2)
                if cell.has_wall(2):
                    buffer[cy][cx + 1] = "█"
                # South wall (bit 4)
                if cell.has_wall(4):
                    buffer[cy + 1][cx] = "█"
                # West wall (bit 8)
                if cell.has_wall(8):
                    buffer[cy][cx - 1] = "█"

                # Cell centers
                coord = (x, y)
                if coord == entry:
                    buffer[cy][cx] = "\033[95mE\033[0m"  # Magenta Entry
                elif coord == exit_pos:
                    buffer[cy][cx] = "\033[91mX\033[0m"  # Red Exit
                elif cell.is_pattern_42:
                    buffer[cy][cx] = "\033[90m█\033[0m"  # Gray 42 pattern
                elif coord in path_set:
                    buffer[cy][cx] = "\033[94m•\033[0m"  # Blue solution path

        # Print rendered grid with wall color palette
        print("=== A-Maze-ing ===")
        for r in range(buf_h):
            line_str = ""
            for c in range(buf_w):
                ch = buffer[r][c]
                if ch == "█":
                    line_str += f"{wall_color}█{self._reset}"
                else:
                    line_str += ch
            print(line_str)

        # Print menu options
        path_status = "ON" if self.show_path else "OFF"
        print(f"\nPath display: {path_status}")
        print("Menu:")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
