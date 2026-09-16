"""Controller module for managing the A-Maze-ing application flow."""

from src.config_parser import ConfigData, ConfigParser
from src.exporter import MazeExporter
from src.renderer import TerminalRenderer
from mazegen.generator import MazeGenerator


class GameController:
    """Coordinates configuration, generation, solving, and rendering."""

    def __init__(self, config_path: str) -> None:
        """Load configuration and initialize controller state."""
        self.config_path: str = config_path
        parser = ConfigParser(config_path)
        self.config: ConfigData = parser.parse()

        self.renderer: TerminalRenderer = TerminalRenderer()
        self.exporter: MazeExporter = MazeExporter(self.config.output_file)
        self.generator: MazeGenerator | None = None

    def _generate_and_export(
        self, seed: int | None
    ) -> tuple[list[tuple[int, int]], str]:
        """Generate a new maze and export it to the output file."""
        self.generator = MazeGenerator(
            width=self.config.width,
            height=self.config.height,
            entry=self.config.entry,
            exit_pos=self.config.exit,
            perfect=self.config.perfect,
            seed=seed,
        )
        grid = self.generator.generate()
        path_coords, path_str = self.generator.get_solution()

        self.exporter.export(
            grid,
            self.config.entry,
            self.config.exit,
            path_str,
        )
        return path_coords, path_str

    def run(self) -> None:
        """Main interactive loop for the terminal application."""
        path_coords, _ = self._generate_and_export(self.config.seed)

        while True:
            if self.generator is not None:
                self.renderer.render(
                    grid=self.generator.grid,
                    entry=self.config.entry,
                    exit_pos=self.config.exit,
                    path=path_coords,
                )

            try:
                choice = input("\nChoice? (1-4): ").strip()
            except (KeyboardInterrupt, EOFError):
                break

            if choice == "1":
                path_coords, _ = self._generate_and_export(None)
            elif choice == "2":
                self.renderer.toggle_path()
            elif choice == "3":
                self.renderer.rotate_colors()
            elif choice == "4":
                break
