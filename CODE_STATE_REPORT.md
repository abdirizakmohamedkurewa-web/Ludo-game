# Current State of Code Report - Ludo (Python)

This report provides a comprehensive overview of the current architecture, implementation details, testing status, code quality, and potential areas for improvement in the Python Ludo board game repository.

---

## 1. Executive Summary & Repository Overview

The codebase implements a clean, testable, and extendable modular version of the classic **Ludo** board game in Python 3.10+.

### Key Characteristics:
* **Separation of Concerns:** The core game engine (`ludo/`) is entirely headless (pure Python) with no GUI dependencies, making it 100% deterministic and easy to unit test.
* **Dual Interface Support:** Includes both a rich Command Line Interface (CLI) in `apps/cli/` and a Pygame-based Graphical User Interface (GUI) in `apps/gui/`.
* **RNG Determinism:** Seedable dice logic allowing completely reproducible gameplay, debugging, and automated verification.
* **AI Integration:** Implements an extendable bot system with Protocol-defined strategies (Random and Greedy scoring algorithms).
* **High Core Test Coverage:** The core engine (`ludo/`) achieves a stellar **99% test coverage**, validating every nuance of the game's rules and state transitions.

---

## 2. Directory & Component Architecture

Below is the structured catalog of components in the repository:

```
ludo-game/
├─ ludo/                       # Core headless game engine
│  ├─ bots/                    # Bot strategies & decision-making engines
│  │  ├─ base.py               # Strategy protocol interface
│  │  ├─ greedy_bot.py         # Advanced bot utilizing heuristics-based scoring
│  │  ├─ human_bot.py          # Adapter pattern bot for manual human CLI turns
│  │  └─ random_bot.py         # Baseline bot choosing random valid moves
│  ├─ utils/
│  │  └─ constants.py          # Board sizes, entry points, states, and colors
│  ├─ board.py                 # Safe squares, start squares, board layouts
│  ├─ dice.py                  # Standard, optionally seeded 6-sided die
│  ├─ game.py                  # Master game loop/state orchestration
│  ├─ move.py                  # Piece movement, track transitions, capture logic
│  ├─ persistence.py           # Save/load system using JSON serialization
│  ├─ rules.py                 # Moves list generator & rules verification
│  ├─ serialization.py         # Serializable representation dataclasses
│  └─ state.py                 # Live GameState, PlayerState, and PieceState
├─ apps/                       # User interfaces
│  ├─ cli/
│  │  └─ main.py               # CLI runner with support for mixed player roles
│  └─ gui/
│     ├─ board_layout.py       # Cartesian coordinates mapping for GUI renderer
│     ├─ constants.py          # GUI screen sizes, colors, and sizes
│     └─ pygame_app.py         # Full Interactive Pygame application
└─ tests/                      # Extensive test suites (69 unit/integration tests)
```

---

## 3. Deep-Dive: Core Engine (`ludo/`)

The core engine is structured around **Domain-Driven Design (DDD)** principles and a **Finite State Machine (FSM)** for pieces and turn order.

### A. State Representation (`ludo/state.py` & `ludo/piece.py` & `ludo/player.py`)
* **GameState:** Tracks players, current turn player index, last rolled value, consecutive sixes, game over status, and random seed.
* **Piece:** Every player has 4 pieces. Each piece maintains:
  * `id`: 0 to 3
  * `color`: `PlayerColor` Enum (RED, GREEN, YELLOW, BLUE)
  * `state`: `PieceState` Enum (`YARD`, `TRACK`, `HOME_COLUMN`, `HOME`)
  * `position`:
    * `-1` in `YARD`
    * `0-51` on circular `TRACK`
    * `52-57` in color-specific `HOME_COLUMN`
* **Player:** Holds a player’s color, role (`"human"`, `"random"`, or `"greedy"`), and list of pieces.

### B. Game Rules & Move Computation (`ludo/rules.py` & `ludo/move.py`)
* **`Rules.get_legal_moves`:** Computes all legal movements for the active player based on the active roll:
  * Pieces in `YARD` can only move to their start track square if they roll a `6`.
  * Path checking ensures pieces do not bypass an opponent's blocking square (if `use_blocking_rule` is enabled).
  * Exact roll requirements are enforced to transition into the final `HOME` spot.
* **Capturing:** If a piece lands on an opponent's non-safe square, the opponent's piece transitions back to `YARD` (`state = PieceState.YARD`, `position = -1`).
* **Safe Squares:** Eight designated safe track squares where capturing is disallowed.
* **Blocking Rule:** If two same-colored pieces occupy the same track square, they form a blockade. Opponent pieces can neither pass nor land on this block.

### C. Game Orchestration (`ludo/game.py`)
* Coordinates turns, consecutive 6s turn-forfeiting (after three 6s, the turn automatically passes, if enabled), extra turn rewards on 6s, and automated bot vs. human gameplay loop.

### D. Serialization & Persistence (`ludo/serialization.py` & `ludo/persistence.py`)
* Implements a schema-versioned serialization layer converting domain dataclasses into intermediate serializable dataclasses, which are exported to/imported from JSON files via `json.dump` / `json.load`.

### E. Bot AI Strategy Framework (`ludo/bots/`)
All bot strategies implement the `Strategy` protocol:
1. **RandomBot:** Chooses a random legal move.
2. **GreedyBot:** Evaluates potential outcomes on a deep-copied simulator game state. Moves are ranked according to high-priority objectives:
   * **Priority 4:** Winning/Home entry move
   * **Priority 3:** Capturing an opponent's piece
   * **Priority 2:** Exiting the Yard onto the Track
   * **Priority 1:** Furthest progressed piece movement
   * **Priority 0:** Other movements
   * *Tie-breaker:* Selects the piece with the higher destination position.

---

## 4. User Interfaces (`apps/`)

### Command-Line Interface (`apps/cli/`)
An interactive CLI loop. It supports mixing and matching human players with `random` or `greedy` bots via the `--players` startup argument, and loading saved matches with `--load-game`.

### Pygame GUI (`apps/gui/`)
A fully-featured 2D implementation of Ludo using Pygame:
* Maps board logic positions to accurate Cartesian coordinates (grid cells).
* Renders piece stacks visually.
* Animates player turns, highlights legal moves, and enables drag-and-drop or point-and-click piece selection.

---

## 5. Testing & Code Quality Status

### Unit and Integration Tests (`tests/`)
An exhaustive test suite of **69 tests** validates rules, edge cases, bots, game state persistence, packaging, and GUI/CLI interactions.

#### Coverage Metrics:
Running the test suite yields the following results:

```
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
ludo/__init__.py              0      0   100%
ludo/board.py                 6      0   100%
ludo/bots/__init__.py         0      0   100%
ludo/bots/base.py             6      0   100%
ludo/bots/greedy_bot.py      35      0   100%
ludo/bots/human_bot.py       18      0   100%
ludo/bots/random_bot.py       8      0   100%
ludo/dice.py                  9      0   100%
ludo/game.py                 82      3    96%   113, 117, 166
ludo/move.py                 41      2    95%   43, 54
ludo/persistence.py          17      0   100%
ludo/piece.py                15      0   100%
ludo/player.py               19      0   100%
ludo/rules.py                54      0   100%
ludo/serialization.py        23      0   100%
ludo/state.py                26      0   100%
ludo/utils/__init__.py        0      0   100%
ludo/utils/constants.py      11      0   100%
-------------------------------------------------------
TOTAL                       370      5    99%
```

* **Core Engine Coverage (`ludo/`): 99%**
* **Application Interfaces Coverage (`apps/`): 12%** (expected for GUI code, though CLI core interaction paths are covered in integration tests).

### Formatting & Code Quality Tools
The project enforces strict coding standards specified in `pyproject.toml`:
* **Formatting:** `black`
* **Linting:** `ruff` (enforcing Pyflakes, Pycodestyle, Isort, and Flake8-bugbear)
* **Type Checking:** `mypy` (success: no issues found across all packages)

---

## 6. Project Strengths & Architectural Analysis

### Strengths:
1. **Exceptional Test Coverage & Design:** Writing pure Python business rules makes testing board game mechanics completely seamless.
2. **Deterministic Simulation:** The seedable dice and deep-copying in the Greedy bot showcase elegant simulation patterns.
3. **Decoupled Architecture:** Clean boundary between presentation layer (`apps/`) and state rules (`ludo/`).
4. **Strong Typing:** Extensive type hinting and MyPy compliance prevents runtime attribute or type errors.

### Tech Debt & Recommendations for Improvements:
1. **Ruff/Black Adjustments:** A few minor formatting and unused import statements exist in test files and the Pygame application. Standardizing them via `ruff check --fix` and `black .` will improve consistency.
2. **State Mutability:** State copy operations (`copy.deepcopy`) in `GreedyBot` work perfectly but can be resource-intensive. Transitioning to a lighter move simulator or immutable state representation could optimize performance.
3. **Packaging / Distribution:** Currently, the package is structured as editable installable (`ludo-game==1.0.0`), but future releases can bundle assets and configs for seamless PyPI indexing.

---
*Report compiled on: February 2025*
