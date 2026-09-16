#!/usr/bin/env python3
"""Main entry point for the A-Maze-ing application."""

import sys
import time

from mazegen.cell import Cell
from src.controller import GameController
from src.renderer import TerminalRenderer


ANIMATION_DELAY = 0.01


def render_animation_frame(
    renderer: TerminalRenderer,
    grid: list[list[Cell]],
    head: tuple[int, int],
) -> None:
    """Render a single generation animation frame to terminal."""
    renderer.render_generation(grid, head)
    sys.stdout.flush()
    if ANIMATION_DELAY > 0:
        time.sleep(ANIMATION_DELAY)


def main() -> None:
    """Validate command line arguments and launch the maze application."""
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 a_maze_ing.py <config.txt>\n")
        sys.exit(1)

    config_file = sys.argv[1]
    renderer = TerminalRenderer()

    try:
        controller = GameController(config_file)

        if controller.config.animate:
            renderer.clear_screen()

        try:
            controller.run(
                step_callback=(
                    lambda grid, head: render_animation_frame(
                        renderer,
                        grid,
                        head,
                    )
                )
            )
        finally:
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()

    except KeyboardInterrupt:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        sys.stderr.write("\nGeneration interrupted.\n")
        sys.exit(130)

    except Exception as error:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        sys.stderr.write(f"Error: {error}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
