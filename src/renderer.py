import shutil
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen.cell import Cell


class TerminalRenderer:
    def __init__(self) -> None:
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
        self.show_path = not self.show_path

    def rotate_colors(self) -> None:
        self.color_index = (self.color_index + 1) % len(self.palettes)

    def _build_maze_lines(
        self,
        grid: list[list["Cell"]],
        wall_color: str,
        entry: tuple[int, int] | None = None,
        exit_pos: tuple[int, int] | None = None,
        path_set: set[tuple[int, int]] | None = None,
        head: tuple[int, int] | None = None,
    ) -> list[str]:
        height = len(grid)
        width = len(grid[0])
        lines: list[str] = []

        for y in range(height):
            row_top: list[str] = [f"{wall_color}▓{self._reset}"]
            for x in range(width):
                cell = grid[y][x]
                if cell.has_wall(1):
                    row_top.append(f"{wall_color}▓▓{self._reset}")
                else:
                    row_top.append("  ")
                row_top.append(f"{wall_color}▓{self._reset}")
            lines.append("".join(row_top))

            row_mid: list[str] = [
                f"{wall_color}▓{self._reset}"
                if grid[y][0].has_wall(8)
                else " "
            ]
            for x in range(width):
                cell = grid[y][x]
                coord = (x, y)

                if coord == head:
                    content = "\033[95m🌕\033[0m"
                elif coord == entry:
                    content = "\033[95m🛸\033[0m"
                elif coord == exit_pos:
                    content = "\033[91m🐄\033[0m"
                elif cell.is_pattern_42:
                    content = "\033[90m█▓\033[0m"
                elif path_set and coord in path_set:
                    content = "\033[94m •\033[0m"
                else:
                    content = "  "

                row_mid.append(content)
                if cell.has_wall(2):
                    row_mid.append(f"{wall_color}▓{self._reset}")
                else:
                    row_mid.append(" ")
            lines.append("".join(row_mid))

        row_bot: list[str] = [f"{wall_color}▓{self._reset}"]
        for x in range(width):
            cell = grid[height - 1][x]
            if cell.has_wall(4):
                row_bot.append(f"{wall_color}▓▓{self._reset}")
            else:
                row_bot.append("  ")
            row_bot.append(f"{wall_color}▓{self._reset}")
        lines.append("".join(row_bot))

        return lines

    def clear_screen(self) -> None:
        sys.stdout.write("\033[H\033[2J\033[3J\033[?25l")
        sys.stdout.flush()

    def render_generation(
        self,
        grid: list[list["Cell"]],
        head: tuple[int, int],
    ) -> None:
        height = len(grid)
        if height == 0:
            return

        width = len(grid[0])
        if width == 0:
            return

        wall_color = self.palettes[self.color_index]
        maze_lines = self._build_maze_lines(
            grid=grid,
            head=head,
            wall_color=wall_color,
        )

        term_lines = shutil.get_terminal_size().lines
        header = (
                 "╭────────────────────────────────────╮\n"
                 "│        A - M A Z E - I N G         │\n"
                 "╰────────────────────────────────────╯"
              )
        footer_status = "\033[93mGenerating maze...\033[0m"

        total_needed = len(maze_lines) + 3
        if total_needed <= term_lines:
            visible_lines = maze_lines
        else:
            avail = max(5, term_lines - 4)
            head_line_idx = 2 * head[1] + 1
            start = max(
                0,
                min(len(maze_lines) - avail, head_line_idx - avail // 2),
            )
            visible_lines = maze_lines[start : start + avail]

        frame_parts = [
            "\033[H\033[?25l",
            header + "\033[K",
            *(line + "\033[K" for line in visible_lines),
            "\033[K",
            footer_status + "\033[K",
        ]
        sys.stdout.write("\n".join(frame_parts) + "\033[J")
        sys.stdout.flush()

    def render(
        self,
        grid: list[list["Cell"]],
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        path: list[tuple[int, int]],
    ) -> None:
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0

        if width == 0 or height == 0:
            print("Empty maze grid.")
            return

        wall_color = self.palettes[self.color_index]
        path_set = set(path) if (self.show_path and path) else set()

        maze_lines = self._build_maze_lines(
            grid=grid,
            wall_color=wall_color,
            entry=entry,
            exit_pos=exit_pos,
            path_set=path_set,
        )

        path_status = "ON" if self.show_path else "OFF"
        output_parts = [
            "\033[H\033[2J\033[3J\033[?25h",
            "╭────────────────────────────────────╮\n"
            "│        A - M A Z E - I N G         │\n"
            "╰────────────────────────────────────╯",
            *maze_lines,
            f"\nPath display: {path_status}",
            "Menu:",
            "1. Re-generate a new maze",
            "2. Show/Hide path from entry to exit",
            "3. Rotate maze colors",
            "4. Quit",
        ]
        sys.stdout.write("\n".join(output_parts) + "\n")
        sys.stdout.flush()
