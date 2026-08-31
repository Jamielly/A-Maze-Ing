*This project has been created as part of the 42 curriculum by jamsilva, luafranc.*

# A-Maze-ing

![Language](https://img.shields.io/badge/language-Python-blue.svg)
![42](https://img.shields.io/badge/42-A--Maze--ing-black.svg)
![Status](https://img.shields.io/badge/status-Completed-success.svg)
![Norminette](https://img.shields.io/badge/lint-passing-brightgreen.svg)

---

## Description

`A-Maze-ing` is a maze generator written in pure Python (standard library only). It reads a plain text configuration file, generates a random **perfect maze** (exactly one path between any two cells, no loops), writes it to a file using a hexadecimal wall encoding, and displays it in the terminal with an interactive menu.

The maze contains a visible **"42"** drawn with fully closed cells, the outer border is fully walled, and the shortest path from the entry to the exit is computed and saved alongside the maze.

> This implementation covers the mandatory part of the subject only — the bonus (the fully braided, no-dead-end "playable board" mode) was not implemented.

---

## Instructions

### Requirements

The program needs **Python 3.10 or later** and no third-party dependency.

### Usage

```bash
python3 ./a_maze_ing.py config.txt
```

### Compilation / setup

The project uses a `Makefile` to automate the usual tasks:

| Command       | Action                                          |
|---------------|--------------------------------------------------|
| `make install`| Create the virtual environment and install tools |
| `make run`    | Run the program on `config.txt`                   |
| `make lint`   | Run the linter/type checker                       |
| `make clean`  | Remove caches and build artefacts                  |

Every error is reported with a clear message and a non-zero exit status: missing or unreadable file, bad syntax, missing key, invalid value, entry or exit outside the maze, unwritable output file...

### Interactive display

The maze is drawn in the terminal with coloured blocks (walls, corridors, entry, exit, the "42" pattern and the shortest path). The menu offers:

```
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit
```

### Configuration file

One `KEY=VALUE` pair per line (`#` and blank lines are ignored):

| Key           | Mandatory | Value                                          |
|---------------|-----------|-------------------------------------------------|
| `WIDTH`       | yes       | Number of cells per row, `>= 2`                  |
| `HEIGHT`      | yes       | Number of cells per column, `>= 2`               |
| `ENTRY`       | yes       | Entry cell, written `x,y`                        |
| `EXIT`        | yes       | Exit cell, written `x,y`, different from `ENTRY` |
| `OUTPUT_FILE` | yes       | File the maze is written to                      |
| `SEED`        | no        | Integer seed, for a reproducible maze            |

---

## Algorithm

Generation happens in two steps:

### 1. The "42" pattern

The cells drawing the digits are reserved and left fully closed. The drawing is centred so the middle of the maze stays open. If the maze is too small, or the entry/exit lands on the drawing, the pattern is skipped and an error is printed.

### 2. Carving — randomised depth-first search (recursive backtracker)

Starting from the entry, the algorithm walks to a random unvisited neighbour, removes the wall between the two cells, and backtracks when stuck. Reserved cells are never visited. This produces a **spanning tree** of the corridors: every cell is reachable, and there is exactly one path between any two cells — which is precisely a perfect maze.

The shortest path is then found with a **breadth-first search** from the entry.

### Why this algorithm

- Simple, with no failure case, and correct by construction on the hardest requirement: a spanning tree is fully connected and contains no loop.
- Runs in O(cells) with an explicit stack, avoiding the Python recursion limit even on large mazes.
- Produces long winding corridors rather than the short branches typical of Prim's or Kruskal's algorithms.
- Reproducibility is free: a single seeded `random.Random` instance drives the whole generation.

---

## Resources

### References

- [Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm) — Wikipedia, overview of the classic algorithms.
- [Buckblog: Maze Generation — Recursive Backtracking](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking) — reference explanation of the algorithm used here.
- [Spanning tree](https://en.wikipedia.org/wiki/Spanning_tree) — Wikipedia, the graph theory behind perfect mazes.
- Python `random` and `collections.deque` official documentation.

### AI Usage

AI was used to assist with the following tasks:

- **Scaffolding:** initial directory structure and `Makefile` rules.
- **Logic:** assistance in reasoning through the carving (DFS) and shortest-path (BFS) implementation.

All code was manually reviewed, refactored, and tested to ensure full understanding.

---

## Contributions

Both members contributed equally to the core logic.

| Member    | Responsibilities                                   |
|-----------|------------------------------------------------------|
| jamsilva  | *(fill in: e.g. carving logic, config parsing)*     |
| luafranc  | *(fill in: e.g. display/menu, output serialization)*|
