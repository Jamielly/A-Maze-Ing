"""Module responsible for exporting the generated maze data and solution to a file."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen.cell import Cell


class MazeExporter:
    """Handles exporting the maze grid, entry/exit coordinates, and path to a file."""

    def __init__(self, output_file: str) -> None:
        """Initializes the maze exporter with the target output file path.

        Args:
            output_file: Path to the file where the maze will be exported.
        """
        self.output_file: str = output_file

    def export(
        self,
        grid: list[list["Cell"]],
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        path_str: str,
    ) -> None:
        """Exports the maze grid, entry, exit, and solution path to the output file.

        Args:
            grid: The 2D grid matrix of cells representing the maze.
            entry: (x, y) coordinates of the maze entry point.
            exit_pos: (x, y) coordinates of the maze exit point.
            path_str: String representation of the solution path.
        """
        lines: list[str] = []

        for row in grid:
            row_hex = "".join(cell.to_hex() for cell in row)
            lines.append(row_hex)

        lines.append("")
        lines.append(f"{entry[0]},{entry[1]}")
        lines.append(f"{exit_pos[0]},{exit_pos[1]}")
        lines.append(path_str)

        content = "\n".join(lines) + "\n"

        with open(self.output_file, "w", encoding="utf-8") as file:
            file.write(content)
