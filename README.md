*This project has been created as part of the 42 curriculum by jamsilva, luafranc.*

# 🌀 A-Maze-ing

![Language](https://img.shields.io/badge/language-Python_3.10+-blue.svg)
![42](https://img.shields.io/badge/42-A--Maze--ing-black.svg)
![Status](https://img.shields.io/badge/status-Completed-success.svg)
![Bonus](https://img.shields.io/badge/bonus-included-orange.svg)
![Lint](https://img.shields.io/badge/flake8_%2B_mypy-passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

---

## Description

`A-Maze-ing` is a maze generation and visualization system written in pure Python for the 42 curriculum. It reads a key-value configuration file, generates a maze under strict graph-theory and game-design constraints, writes the hex-encoded result to a file, and renders it in an interactive terminal interface.

The generation engine is packaged as an independent, reusable library (`mazegen`) and supports two maze types:

| Mode | `PERFECT` | Result |
|:-----|:---------:|:-------|
| **Perfect maze** | `True` | A mathematical spanning tree — exactly one path between any two cells, no loops, no isolated areas. |
| **Playable board** | `False` | A Pac-Man-style board with open corners, a central starting hub, and multiple independent loops for player mobility — with no 3×3 fully open area anywhere. |

Both modes embed a centered **"42"** pattern made of fully closed cells, and both can be watched being built through a real-time, step-by-step animation of the algorithm.

---

## Instructions

### Requirements

- **Python 3.10 or higher**
- Standard library only (`random`, `typing`, `sys`, `time`, `collections`, …) — no runtime dependency

### Quick start

```bash
python3 a_maze_ing.py config.txt
```

### Makefile automation

| Rule           | Action                                                                 |
|----------------|-------------------------------------------------------------------------|
| `make install` | Creates a virtual environment and installs the dev tools (`flake8`, `mypy`, `build`) |
| `make run`     | Runs the program with the default `config.txt`                           |
| `make build`   | Builds the standalone `mazegen` package into `.whl` and `.tar.gz`        |
| `make lint`    | Runs `flake8` and `mypy` with the flags mandated by the subject          |
| `make clean`   | Removes caches and build artefacts (`__pycache__`, `build`, `dist`, `*.egg-info`) |

### Configuration file

A plain text file of `KEY=VALUE` pairs. Blank lines and lines starting with `#` are ignored.

| Key           | Mandatory | Type       | Description                                | Example                |
|---------------|:---------:|------------|--------------------------------------------|------------------------|
| `WIDTH`       | yes       | `int` ≥ 2  | Grid width, in cells                        | `WIDTH=20`             |
| `HEIGHT`      | yes       | `int` ≥ 2  | Grid height, in cells                       | `HEIGHT=15`            |
| `ENTRY`       | yes       | `x,y`      | Entrance coordinates, inside the grid       | `ENTRY=0,0`            |
| `EXIT`        | yes       | `x,y`      | Exit coordinates, inside the grid           | `EXIT=19,14`           |
| `OUTPUT_FILE` | yes       | `str`      | Destination file for the hex-encoded maze   | `OUTPUT_FILE=maze.txt` |
| `PERFECT`     | yes       | `bool`     | `True` for a perfect maze, `False` for the playable board | `PERFECT=True` |
| `SEED`        | no        | `int`      | Random seed, for reproducible generation    | `SEED=42`              |

### Interactive controls

The maze is rendered with ANSI colours for walls, entrance, exit, the "42" pattern and the solution path.

| Key | Action                            |
|:---:|-----------------------------------|
| `1` | Generate a new maze                |
| `2` | Show / hide the shortest path      |
| `3` | Rotate the wall colour theme       |
| `4` | Quit                               |

---

## Reusable Module — `mazegen`

All generation logic lives in the standalone `mazegen/` package. It builds into a wheel (`mazegen-1.0.0-py3-none-any.whl`) and installs into any Python environment.

### Build and install

```bash
# Build the wheel at the root of the repository
python3 -m build

# Install it into a virtual environment
pip install dist/mazegen-1.0.0-py3-none-any.whl
```

### Basic usage

```python
from mazegen import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit_pos=(19, 14),
    perfect=True,
    seed=42,
)

grid = generator.generate()                        # list[list[Cell]]
path_coords, direction_str = generator.get_solution()

print(f"Path directions: {direction_str}")         # e.g. "EESSSWW..."
```

### Real-time animation hook

`generate()` accepts an optional `step_callback` of type `Callable[[list[list[Cell]], tuple[int, int]], None]`, letting any external renderer animate the carving step by step:

```python
def my_animation_callback(current_grid, current_head_pos):
    # Redraw the screen and highlight the drill head
    draw_frame(current_grid, current_head_pos)

generator.generate(step_callback=my_animation_callback)
```

This is what keeps `mazegen` fully decoupled from the terminal UI.

---

## Algorithm & Technical Choices

### Chosen algorithm — randomized DFS (recursive backtracker)

Generation uses an **iterative** Depth-First Search driven by an explicit stack (`list[tuple[int, int]]`).

1. **"42" pattern reservation** — the central cells forming the digits are flagged as reserved (`is_pattern_42 = True`) and initialized fully closed (`walls = 15`).
2. **Carving the corridors** — from the entry cell, the algorithm picks a random unvisited neighbour (never a reserved cell), clears the shared wall bit, marks it visited and pushes it onto the stack; when stuck, it backtracks with `stack.pop()`.
3. **Loop carving (`PERFECT=False`)** — extra connections are carved deterministically around the four corners and the central hub, then further internal walls are opened at random to create independent loops, while `_has_3x3_open()` rejects any move that would produce a 3×3 fully open area.
4. **Wall consistency** — a final pass (`_enforce_wall_consistency()`) guarantees adjacent cells agree on their shared wall bits.

The shortest path is then extracted by `MazeSolver` and returned both as coordinates and as a direction string.

### Why recursive backtracking

- **Spanning tree guarantee** — DFS builds a spanning tree by construction, so perfect mode is 100% connected with no loops and no isolated corridors.
- **Explicit stack** — sidesteps Python's recursion limit, so grids of 100×100 and beyond generate safely with predictable memory use.
- **Aesthetic quality** — produces long, winding corridors instead of the short, noisy branches typical of Prim's or Kruskal's algorithms.

### Wall encoding

Each cell stores its closed walls as a 4-bit mask — `N=1`, `E=2`, `S=4`, `W=8` — so a fully closed cell is `15` (`0xF`) and the maze serializes directly to the hexadecimal format required by the subject.

---

## Bonus Features

- **⭐ Real-time algorithm animation** — the DFS drill head carving the maze, rendered live in the terminal.
- **⭐ Playable board mode** — passes the official `maze_analyzer.py` test suite for both `PERFECT=True` and `PERFECT=False`.

---

## Resources

### References

- [Maze generation algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm) — Wikipedia
- [Jamis Buck — Maze Generation: Recursive Backtracking](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking)
- [Python Packaging User Guide](https://packaging.python.org/)

### AI Usage

AI was used as an educational assistant for:

- **Architecture planning** — shaping the `StepCallback` mechanism that decouples `mazegen` from the terminal UI.
- **Bitmask verification** — checking the consistency of the 4-bit wall encoding (`N=1`, `E=2`, `S=4`, `W=8`).
- **Documentation** — formatting this README against the 42 evaluation guidelines.

All AI-suggested code was manually reviewed, refactored, type-annotated (`mypy`) and tested.

---

## Team & Project Management

### Roles

| Member   | Login      | Responsibilities                                                                                     |
|----------|------------|------------------------------------------------------------------------------------------------------|
|  Luana   | `luafranc` | `mazegen` core generator, bitmask encoding, DFS carving, loop generation, `pyproject.toml` packaging |
| Jamielly | `jamsilva` | `a_maze_ing.py` CLI, config parser, ANSI terminal rendering, interactive menu, animation callbacks   |

### Planning & evolution

- **Initial plan:** write a monolithic script first, extract the module at the end.
- **What actually happened:** `mazegen` was decoupled early into a standalone package with clean interfaces (`MazeGenerator`, `Cell`, `MazeSolver`). Adding the step callbacks and the terminal animation afterwards required no refactor of the core logic.

### Lessons learned

- **What worked well:** the explicit DFS stack, and defining the `StepCallback` interface up front — together they kept the library and the renderer fully independent.
- **Future improvements:** MiniLibX (MLX) graphical rendering, and support for additional generation algorithms such as Kruskal's.

---

## License

Released under the MIT License — see [`LICENSE.md`](LICENSE.md). The `mazegen` module is explicitly licensed for reuse in future 42 projects.
