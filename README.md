*This project has been created as part of the 42 curriculum by luafranc and jamsilva.*

# A-Maze-ing

## Description
A-Maze-ing is an academic project developed at 42 that explores maze generation, pathfinding algorithms, graph theory, and software packaging in Python.

The program reads configuration parameters, generates a maze (either a single-path perfect maze or a Pac-Man playable board with loops), displays the result in the terminal with ANSI colors, and exports the maze structure and shortest path solution to a text file in hexadecimal format.

## Instructions

### 1. Environment Setup
Create and activate a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Code Quality & Linting
Run the mandatory linters to ensure full compliance with 42 code standards:
```bash
flake8 .
mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

### 3. Build & Install Reusable Package
Build the standalone `mazegen` package into wheel (`.whl`) and source archive (`.tar.gz`):
```bash
python3 -m pip install --upgrade build
python3 -m build
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### 4. Running the Application
Execute the main script with a configuration file:
```bash
python3 a_maze_ing.py config.txt
```

---

## Configuration File Format
The configuration file requires `KEY=VALUE` pairs. Lines starting with `#` are treated as comments.

### Mandatory Keys:
- `WIDTH`: Width of the maze grid (positive integer).
- `HEIGHT`8�Height of the maze grid (positive integer).
- `ENTRY`: Coordinates of the entry cell in `x,y` format.
- `EXIT`: Coordinates of the exit cell in `x,y` format.
- `OUTPUT_FILE`: Path of the destination text file.
- `PERFECT`: Boolean (`True` for single-path maze, `False` for Pac-Man playable board).
- `SEED`: Optional integer for random seed reproducibility.

---

## Algorithm Choice & Justification

### Generation Algorithm: DFS with Iterative Backtracking
- **Why DFS?** Depth-First Search with backtracking naturally produces a spanning tree across the grid, guaranteeing full connectivity and zero isolated cells without relying on Python's recursion limit.
- **Pac-Man Loop Injection:** When `PERFECT=False`, the algorithm opens the four corners, central area, and strategically removes dead-end walls while enforcing a strict check to prevent open areas of 3x3 or larger.

### Pathfinding Algorithm: Breadth-First Search (BFS)
- **Why BFS?** In an unweighted grid, BFS explores cell distances layer-by-layer, mathematically guaranteeing the shortest path from entry to exit.

---

## Reusable Module (`mazegen`)

The `mazegen package is completely standalone and independent of the CLI/renderer.

### Basic Example Usage:
@``python
from mazegen import MazeGenerator

venerator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit_pos=(19, 14),
    perfect=False,
    seed=42,
)

grid = generator.generate()
path_coords, path_str = generator.get_solution()

print(f"Shortest path steps: {len(path_coords)}")
print(f"Path directions: {path_str}")
```

"---

## Team & Project Management
- **Role:** Solo project developed by `luafranc`.
- **Planning:**
  1. Module `cell.py` and bitmask wall structure.
  2. Configuration parser and error handling.
  3. Generation algorithm (DFS) & Pac-Man loop logic.
  4. Solver algorithm (BFS).
  5. ASCII terminal renderer & interactive menu.
  6. Packaging (`pyproject.toml`) and documentation.
- **Tools Used:** VS Code, mypy, flake8, git, Python 3.10+.

---

## Resources & AI Usage
- **References:** IME USP Graph Algorithms (DFS & BFS), Cormen's *Introduction to Algorithms*.
- **AI Usage:** Artificial Intelligence was used as an architectural advisor and code assistant for structuring docstrings, formatting type hints, and organizing packaging specifications.
