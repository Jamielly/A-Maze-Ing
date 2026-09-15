"""Exporter module for saving generated maze data to a text file."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mazegen.cell import Cell


class MazeExporter:
    """Exports maze structure and solution data to an output file."""

    def __init__(self, output_file: str) -> None:
        """Initialize the exporter with an output file path."""
        self.output_file: str = output_file

    def export(
        self,
        grid: list[list["Cell"]],
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        path_str: str,
    ) -> None:
        """Save the maze structure and solution string to the output file."""
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
