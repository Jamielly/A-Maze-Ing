#!/usr/bin/env python3
"""Main entry point for the A-Maze-ing application."""

import sys
from src.controller import GameController


def main() -> None:
    """Validate command line arguments and launch the maze application."""
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 a_maze_ing.py <config.txt>\n")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        controller = GameController(config_file)
        controller.run()
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
