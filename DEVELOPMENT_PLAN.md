# Granular Development Plan for Ludo

This document provides a detailed, step-by-step development plan for the Python Ludo project. It expands on the high-level roadmap in `README.md`.

---

## Milestone 0: Project Skeleton & Core Stubs

**Goal:** Set up the basic project structure, dependencies, and CI/CD pipeline. The game won't be playable, but the foundation will be in place.

-   **Task 0.1: Initialize Git Repository**
    -   [x] Create `.gitignore` for Python (`__pycache__/`, `.venv/`, etc.).
    -   [x] Add `LICENSE` file (e.g., MIT).
-   **Task 0.2: Set up `pyproject.toml`**
    -   [x] Configure `black` for code formatting.
    -   [x] Configure `ruff` for linting.
    -   [x] Configure `mypy` for static type checking.
    -   [x] Configure `pytest` with initial paths.
-   **Task 0.3: Create Directory Structure**
    -   [x] `ludo/`: for the core game engine.
    -   [x] `apps/cli/`: for the command-line interface.
    -   [x] `tests/`: for all unit and integration tests.
    -   [x] `tests/fixtures/`: for test data.
-   **Task 0.4: Define Core Data Models (Stubs)**
    -   [x] `ludo/state.py`: Create `GameState`, `PlayerState`, `PieceState` dataclasses (initially empty).
    -   [x] `ludo/piece.py`: Define `Piece` class with basic attributes (color, id, state).
    -   [x] `ludo/player.py`: Define `Player` class (color, list of pieces).
-   **Task 0.5: Create Core Logic Stubs**
    -   [x] `ludo/dice.py`: Create `Dice` class with a `roll()` method (can be hardcoded to return 1 for now).
    -   [x] `ludo/rules.py`: Create `Rules` class with an empty `legal_moves()` method.
    -   [x] `ludo/board.py`: Define board constants (e.g., track length) in `ludo/utils/constants.py`.
    -   [x] `ludo/game.py`: Create `Game` class with an `__init__` method to set up players.
-   **Task 0.6: Basic CLI Application**
    -   [x] `apps/cli/main.py`: Create a `main` function that initializes a `Game` object and prints a "Hello Ludo" message.
    -   [x] Add `argparse` for future CLI arguments (`--players`, `--seed`).
-   **Task 0.7: Setup CI/CD**
    -   [x] Create `.github/workflows/ci.yml`.
    -   [x] Add jobs for linting, type checking, and running tests on Python 3.10+.
    -   [x] Ensure the initial (empty) test suite runs and passes.

---

## Milestone 1: Implement Complete Game Rules

**Goal:** Implement all core Ludo rules to make the game fully playable from the CLI.

-   **Task 1.1: Implement Dice Logic**
    -   [x] Make `Dice.roll()` return a random number from 1-6.
    -   [x] Add seeding capability for reproducible tests.
-   **Task 1.2: Implement Piece Movement**
    -   [x] Define piece states: `YARD`, `TRACK`, `HOME_COLUMN`, `HOME`.
    -   [x] Implement logic to move a piece along the main track.
-   **Task 1.3: Implement "Enter from Yard" Rule**
    -   [x] A piece can only move from `YARD` to its entry square if a `6` is rolled.
    -   [x] The move from `YARD` consumes the `6` (no further movement on that roll).
-   **Task 1.4: Implement Captures**
    -   [x] If a piece lands on a square occupied by an opponent, the opponent's piece is sent back to its `YARD`.
    -   [x] Implement "safe squares" where captures are not possible.
-   **Task 1.5: Implement Home Column & Winning**
    -   [x] Implement the logic for a piece to enter its home column.
    -   [x] Require an **exact roll** to move a piece into the final `HOME` position.
    -   [x] A player wins when all 4 of their pieces are in the `HOME` position.
-   **Task 1.6: Implement "Extra Turn" Rule**
    -   [x] Rolling a `6` grants the player an additional turn.
    -   [x] (Configurable) Implement the "three consecutive 6s forfeit turn" rule.
-   **Task 1.7: Implement Blocking (Optional Rule)**
    -   [x] (Configurable) If two pieces of the same color are on the same square, they form a block.
    -   [x] Opponent pieces cannot pass a block.
-   **Task 1.8: Comprehensive Tests for Rules**
    -   [x] Write unit tests for every rule and edge case in `tests/test_rules.py`.

---

## Milestone 2: Develop Bot Strategies

**Goal:** Create AI players that can play the game automatically.

-   **Task 2.1: Define Bot Strategy Interface**
    -   [x] In `ludo/bots/base.py`, define a `Strategy` protocol with a `choose_move()` method.
-   **Task 2.2: Implement `RandomBot`**
    -   [ ] `ludo/bots/random_bot.py`: Create a bot that chooses a random move from the list of legal moves.
    -   [ ] Integrate the `RandomBot` into the CLI as a player option.
-   **Task 2.3: Implement `GreedyBot`**
    -   [ ] `ludo/bots/greedy_bot.py`: Create a bot with a simple evaluation function.
    -   [ ] The evaluation should prioritize moves in this order:
        1.  Move a piece into the `HOME` position.
        2.  Capture an opponent's piece.
        3.  Move a piece out of the `YARD`.
        4.  Move the piece that is furthest along the track.
-   **Task 2.4: Test Bot Logic**
    -   [ ] `tests/test_bots.py`: Write tests to ensure bots make predictable choices in specific scenarios.

---

## Milestone 3: Persistence (Save/Load Game)

**Goal:** Allow users to save a game in progress and load it later.

-   **Task 3.1: Design Serialization Format**
    -   [ ] Use JSON for human-readable save files.
    -   [ ] Define the schema for `GameState`: include player positions, current turn, dice seed, etc.
    -   [ ] Add a `schema_version` field for future-proofing.
-   **Task 3.2: Implement Save Logic**
    -   [ ] `ludo/persistence.py`: Create a `save_game(state, filepath)` function.
    -   [ ] Convert the `GameState` dataclass to a dictionary and write to a JSON file.
-   **Task 3.3: Implement Load Logic**
    -   [ ] `ludo/persistence.py`: Create a `load_game(filepath)` function.
    -   [ ] Read the JSON file and reconstruct the `GameState` object.
-   **Task 3.4: Integrate into CLI**
    -   [ ] Add CLI commands to save and load games (e.g., an in-game command or startup flags).

---

## Milestone 4: GUI (Optional)

**Goal:** Create a graphical user interface for the game using Pygame.

-   **Task 4.1: Basic Board Rendering**
    -   [ ] `apps/gui/pygame_app.py`: Create a Pygame window.
    -   [ ] Draw the Ludo board, including squares, yards, and home columns.
    -   [ ] Draw pieces at their correct positions based on the `GameState`.
-   **Task 4.2: Game State Visualization**
    -   [ ] Display the current player's turn.
    -   [ ] Show the result of a dice roll.
    -   [ ] Highlight legal moves when a piece is selected.
-   **Task 4.3: User Interaction**
    -   [ ] Implement mouse clicks to roll the dice.
    -   [ ] Implement mouse clicks to select a piece to move.
-   **Task 4.4: Animations (Simple)**
    -   [ ] Animate the dice roll.
    -   [ ] Animate piece movement from one square to another.
-   **Task 4.5: Game Over Screen**
    -   [ ] Display a message when a player wins the game.

---

## Milestone 5: Polish & Release

**Goal:** Finalize documentation, packaging, and prepare for a version 1.0 release.

-   **Task 5.1: Finalize Documentation**
    -   [ ] Update `README.md` with instructions for all features (CLI, GUI, bots).
    -   [ ] Add API documentation using docstrings.
    -   [ ] Create a `CONTRIBUTING.md` file with guidelines for developers.
-   **Task 5.2: Code Cleanup**
    -   [ ] Perform a final pass of linting and formatting.
    -   [ ] Refactor any complex or unclear parts of the code.
    -   [ ] Ensure test coverage is high (e.g., >90%).
-   **Task 5.3: Packaging for Distribution (Optional)**
    -   [ ] Configure `pyproject.toml` for PyPI.
    -   [ ] Create a source distribution (`sdist`) and wheel.
    -   [ ] Test installation from the created package.
-   **Task 5.4: Tag Version 1.0**
    -   [ ] Create a `v1.0.0` git tag.
    -   [ ] Create a release on GitHub with release notes.
