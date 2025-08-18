# Ludo (Python) — Developer README

> A clean, testable, and extendable implementation of the classic **Ludo** board game in Python.  
> This README is your end-to-end guide for setting up, understanding the architecture, contributing, and shipping.

---

## Table of Contents

- [Project Vision](#project-vision)
- [Game Rules (Summary)](#game-rules-summary)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Clone & Environment](#clone--environment)
  - [Install Dependencies](#install-dependencies)
  - [Run the App](#run-the-app)
  - [Run Tests](#run-tests)
- [Core Architecture](#core-architecture)
  - [Domain Model](#domain-model)
  - [Turn State Machine](#turn-state-machine)
  - [Board Coordinates & Paths](#board-coordinates--paths)
  - [Rules Engine](#rules-engine)
  - [Persistence (Save/Load)](#persistence-saveload)
  - [Bots & Strategy](#bots--strategy)
- [Coding Standards](#coding-standards)
  - [Style & Linting](#style--linting)
  - [Static Types](#static-types)
  - [Pre-commit Hooks](#pre-commit-hooks)
- [Testing Strategy](#testing-strategy)
- [Continuous Integration](#continuous-integration)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [FAQ & Troubleshooting](#faq--troubleshooting)
- [License](#license)

---

## Project Vision

- **Goals**
  - A reliable **core rules engine** for Ludo with **100% deterministic logic** and a clean API.
  - A simple **CLI** interface first; a **Pygame GUI** as an optional, separate layer.
  - **Extensibility**: custom variants (house rules), AI bots, network play later.
  - **Quality**: tested, typed, and CI-verified.

- **Non-Goals (initially)**
  - Networked multiplayer (may come later).
  - 3D graphics or complex animations.
  - Cloud backend.

---

## Game Rules (Summary)

> Standard Ludo for **2–4 players**, each with **4 pieces**.

- **Objective**: Move all your pieces from your **Yard** to **Home** by circling the board and entering your **home column**.
- **Starting a piece**: You must roll a **6** to move a piece from Yard to its **Entry square** (start square on the main track).
- **Movement**: Roll a die (1–6) and move one **eligible** piece forward that many squares along your track.
- **Extra turns**: Rolling a **6** grants another roll; three consecutive 6s **forfeit** the turn (configurable).
- **Captures**: Landing exactly on an opponent’s piece **captures** it (sends it back to their Yard), except on **safe squares**.
- **Safe squares**: Typically marked positions (often entry squares) where pieces **cannot be captured**.
- **Entering home column**: After completing one full loop, pieces enter a color-specific **home column** and require **exact rolls** to reach the **Home**.
- **Blocking**: Two of your pieces on the same square may **block** the square (optional rule: others cannot pass through).

> This project will encode **standard rules** and allow toggling common **variants** via configuration.

---

## Tech Stack

- **Language**: Python ≥ 3.10
- **Core**: Pure Python (no GUI deps)
- **CLI**: `argparse` / `rich` (optional for nice output)
- **GUI (optional)**: `pygame`
- **Testing**: `pytest`, `pytest-cov`
- **Quality**: `ruff` (lint), `black` (format), `mypy` (types), `pre-commit`
- **CI**: GitHub Actions

---

## Repository Structure

ludo-game/ ├─ ludo/                     # Core game engine (pure Python) │  ├─ init.py │  ├─ game.py                # Game orchestration (turns, state machine) │  ├─ board.py               # Board geometry, squares, paths │  ├─ rules.py               # Move validation, capture rules, safe squares │  ├─ player.py              # Player entity, color, pieces │  ├─ piece.py               # Piece entity & transitions │  ├─ dice.py                # Dice abstraction (seedable for tests) │  ├─ state.py               # dataclasses for GameState, TurnState, etc. │  ├─ persistence.py         # Save/load (JSON) │  ├─ bots/                  # Simple AI strategies │  │  ├─ base.py │  │  ├─ random_bot.py │  │  └─ greedy_bot.py │  └─ utils/ │     └─ constants.py        # safe squares, paths, colors, etc. │ ├─ apps/ │  ├─ cli/ │  │  ├─ init.py │  │  └─ main.py             # CLI entrypoint, human vs human/bot │  └─ gui/ │     ├─ init.py │     └─ pygame_app.py       # Optional Pygame GUI (later milestone) │ ├─ tests/ │  ├─ test_rules.py │  ├─ test_board.py │  ├─ test_game.py │  ├─ test_bots.py │  └─ fixtures/ │     └─ sample_states.json │ ├─ requirements.txt ├─ requirements-dev.txt ├─ README.md ├─ pyproject.toml            # tool configs (ruff/black/mypy/pytest) ├─ .gitignore └─ LICENSE

> **Note**: Start minimal (core + CLI). Add GUI and bots as milestones.

---

## Getting Started

### Prerequisites
- Python **3.10+**
- Git
- (Optional) `make` for convenience commands

### Clone & Environment

**Linux/Mac**
```bash
git clone https://github.com/<your-username>/ludo-game.git
cd ludo-game
python -m venv .venv
source .venv/bin/activate

Windows (PowerShell)

git clone https://github.com/<your-username>/ludo-game.git
cd ludo-game
py -m venv .venv
.venv\Scripts\Activate.ps1

Install Dependencies

# Runtime only
pip install -r requirements.txt

# Dev tools (linters, tests, type checks)
pip install -r requirements-dev.txt

# Optional: set up pre-commit hooks
pre-commit install

Run the App

CLI (human vs random bot example)

python -m apps.cli.main --players human random --seed 42

CLI Help

python -m apps.cli.main --help

Future GUI (after milestone)

python -m apps.gui.pygame_app

Run Tests

pytest -q
pytest --maxfail=1 --disable-warnings -q
pytest --cov=ludo --cov-report=term-missing


---

Core Architecture

Domain Model

Game
Controls lifecycle: setup → turns → end state. Holds GameState, players, dice, and rules engine.

Board
Encapsulates geometry: main circular track (0..51), safe squares, entry squares, home columns (per color), home.

Rules
Validates moves, applies captures/blocks, extra turns, exact-home rules, and variants via config.

Player
Color (Red/Blue/Green/Yellow), pieces, and decision provider (human input or bot strategy).

Piece
State machine: YARD → TRACK → HOME_ENTRY → HOME_COLUMN → HOME.

Dice
Seedable RNG for reproducible tests; supports rule variants (e.g., re-roll on 6).

Bots
Strategies that pick moves given a View of the current GameState (no cheating).


> Design Principle: Keep UI separate from core rules. The ludo/ package must be headless and testable.



Turn State Machine

[START_TURN]
    ↓
[ROLL_DICE] → (die=6?) → grant extra_roll flag
    ↓
[COMPUTE_LEGAL_MOVES]
    ↓ (none)
[NO_MOVE_AVAILABLE] → [END_TURN]
    ↓ (some)
[CHOOSE_MOVE] (human or bot)
    ↓
[APPLY_MOVE] (advance, capture, block, home-entry)
    ↓
[CHECK_WIN] → if player has all pieces HOME → [END_GAME]
    ↓
[EXTRA_ROLL?] → yes → loop back to [ROLL_DICE]
    ↓
[END_TURN] → next player

Configurable variant: three consecutive 6s = turn forfeited.


Board Coordinates & Paths

Main track: 52 squares (indexed 0..51 clockwise).

Entry squares (per color): the square where a piece enters from Yard on a 6.
Example (conventional; configurable):

Red: 0, Blue: 13, Yellow: 26, Green: 39


Safe squares: Typically all entry squares + home-entry squares (configurable).

Home entry: After completing a loop, each color branches into a home column of 6 squares requiring exact rolls.

Blocking (optional): two same-color pieces on a square may form a block that cannot be captured and optionally cannot be passed.


Implementation tips:

Represent positions as a tagged union:

@dataclass(frozen=True)
class Pos:
    kind: Literal["YARD","TRACK","HOME_ENTRY","HOME_COL","HOME"]
    index: int | None          # TRACK index 0..51, HOME_COL index 0..5, else None

Maintain mappings for each color:

entry_index[color] -> int

home_entry_index[color] -> int

home_path[color] -> list[int] (indices within the home column)



Rules Engine

Key invariants:

A move is legal iff:

The piece is not already in HOME,

The die roll can place it into a valid next position,

If moving from YARD, die must be 6,

Moving into HOME requires an exact roll,

Landing on an opponent on a non-safe square captures them,

Blocks (if enabled) cannot be passed or captured.



Rules API (illustrative):

class Rules:
    def legal_moves(self, state: GameState, player: Player, roll: int) -> list[Move]: ...
    def apply(self, state: GameState, move: Move) -> GameState: ...

Persistence (Save/Load)

Format: JSON snapshot via dataclasses.asdict.

Save files include: RNG seed, current player, turn counters (for 6s), positions, config, history.

Keep forward-compatibility with a schema_version field.


Bots & Strategy

RandomBot: picks a random legal move.

GreedyBot: scoring function prioritizing:

Entering from Yard,

Captures,

Progress towards Home,

Avoiding capture risk (simple lookahead).


Plug via strategy interface:


class Strategy(Protocol):
    def choose_move(self, view: ReadOnlyGameView, roll: int) -> Move | None: ...


---

Coding Standards

Style & Linting

black for formatting.

ruff for linting (E, F, I, and selected B rules).

Run locally:

ruff check .
black --check .


Static Types

Use mypy (strict enough to catch mistakes; allow gradual typing).

mypy ludo apps


Pre-commit Hooks

Install once:

pre-commit install

Hooks:

black, ruff, mypy (as local hook or on CI), trailing-whitespace, end-of-file-fixer.



Minimal pyproject.toml (example):

[tool.black]
line-length = 100
target-version = ["py310"]

[tool.ruff]
line-length = 100
select = ["E","F","I","B"]
ignore = []

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"


---

Testing Strategy

Unit tests for: rules, board transitions, dice, piece state machine.

Property tests (optional): invariants like “no piece teleports”, “pieces inside HOME never move”.

Determinism: seed the RNG for reproducible outcomes.

Coverage: target ≥90% on ludo/ package.


Examples:

pytest
pytest --cov=ludo --cov-report=term-missing


---

Continuous Integration

Use GitHub Actions workflow (save as .github/workflows/ci.yml):

name: CI

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - run: python -m pip install --upgrade pip
      - run: pip install -r requirements.txt
      - run: pip install -r requirements-dev.txt
      - run: ruff check .
      - run: black --check .
      - run: mypy ludo apps
      - run: pytest --cov=ludo --cov-report=xml
      - uses: codecov/codecov-action@v4
        if: always()
        with:
          files: ./coverage.xml
          fail_ci_if_error: false


---

Roadmap

[ ] M0 — Skeleton

[ ] Package layout, Game/Board/Rules stubs

[ ] Basic CLI loop (human vs random bot)

[ ] Seedable dice

[ ] Unit test harness


[ ] M1 — Complete Rules

[ ] Entering from Yard on 6

[ ] Captures & safe squares

[ ] Home column with exact rolls

[ ] Consecutive 6s handling (configurable)

[ ] Blocking (toggle)


[ ] M2 — Bots

[ ] RandomBot

[ ] GreedyBot

[ ] Basic evaluation metrics


[ ] M3 — Persistence

[ ] Save/Load JSON

[ ] Deterministic replay (optional)


[ ] M4 — GUI (Optional)

[ ] Pygame board rendering

[ ] Mouse interactions, animations

[ ] Accessibility/high-contrast


[ ] M5 — Polish

[ ] Docs & examples

[ ] Packaging (optional: publish to PyPI)

[ ] Performance profiling (if needed)




---

Contributing

1. Fork the repo, create a feature branch:

git checkout -b feat/<short-description>


2. Keep commits clear; use Conventional Commits:

feat:, fix:, refactor:, docs:, test:, chore:



3. Ensure green CI: lint, type-check, tests.


4. Open a Pull Request with a concise description, screenshots (for GUI), and test notes.



Code Review Checklist

Business logic lives in ludo/, not in UI.

No side effects in pure rule functions.

Tests for new rules & edge cases.

Types & docstrings for public APIs.



---

FAQ & Troubleshooting

Q: Which Python version is required?
A: Python 3.10+. If you see match/case syntax errors, you’re likely on an older Python.

Q: ModuleNotFoundError when running the CLI.
A: Ensure you’re at the project root and the venv is active. Run with python -m apps.cli.main ....

Q: Windows ANSI colors look odd.
A: Use the basic CLI (no colors) or install colorama. We keep colors optional.

Q: How do I seed the dice for reproducible games?
A: Pass --seed <int> on the CLI; tests should seed via fixtures.

Q: Can I change safe squares or entry points?
A: Yes—update ludo/utils/constants.py or expose a config file (future enhancement).


---

License

This project is licensed under the MIT License. See LICENSE for details.


---

Appendix: Minimal Bootstraps

apps/cli/main.py (sketch)

from ludo.game import Game
from ludo.dice import Dice
from ludo.bots.random_bot import RandomBot

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--players", nargs="+", default=["human","random"])
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args()

    dice = Dice(seed=args.seed)
    players = []
    for role in args.players:
        players.append(role)  # "human" or Strategy instance ("random")

    game = Game(players=players, dice=dice)
    game.loop_cli()  # human input via stdin; bots via strategy

if __name__ == "__main__":
    main()

requirements.txt (initial)

# runtime

requirements-dev.txt

pytest
pytest-cov
black
ruff
mypy
pre-commit

Happy building! 🎲



