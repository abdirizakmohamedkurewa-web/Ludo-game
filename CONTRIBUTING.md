# Contributing to Ludo (Python)

First off, thank you for considering contributing to this project! We welcome any contributions that help make this a better Ludo implementation.

This document provides guidelines for contributing to the project. Please read it carefully to ensure a smooth and effective contribution process.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Style Guides](#style-guides)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Styleguide](#python-styleguide)
- [Code Review Checklist](#code-review-checklist)

## Code of Conduct

This project and everyone participating in it is governed by a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior. (Note: `CODE_OF_CONDUCT.md` is a placeholder and will be added later).

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please ensure the bug was not already reported by searching on GitHub under [Issues](https://github.com/user/repo/issues). If you're unable to find an open issue addressing the problem, open a new one. Be sure to include a title and clear description, as much relevant information as possible, and a code sample or an executable test case demonstrating the expected behavior that is not occurring.

### Suggesting Enhancements

If you have an idea for an enhancement, please open an issue to discuss it. This allows us to coordinate efforts and ensure the enhancement fits with the project's goals.

### Pull Requests

1.  **Fork the repository** and create your branch from `main`:
    ```bash
    git checkout -b feat/your-feature-name
    ```
2.  **Make your changes**. Ensure you add tests for any new features or bug fixes.
3.  **Ensure the test suite passes** and the code is linted correctly:
    ```bash
    # Run tests
    pytest
    # Check formatting and linting
    black .
    ruff check .
    mypy ludo apps
    ```
4.  **Keep your commits clear and descriptive**. Follow the [Git Commit Messages](#git-commit-messages) style guide.
5.  **Open a Pull Request** with a concise description of your changes. If it's a visual change, include screenshots. Describe the testing you've done.

## Development Setup

### Prerequisites

-   Python 3.10+
-   Git

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/<your-username>/ludo-game.git
    cd ludo-game
    ```
2.  **Create and activate a virtual environment**:
    ```bash
    # Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate

    # Windows
    py -m venv .venv
    .venv\Scripts\Activate.ps1
    ```
3.  **Install dependencies**:
    ```bash
    # Install runtime dependencies
    pip install -r requirements.txt

    # Install development dependencies
    pip install -r requirements-dev.txt
    ```
4.  **(Optional) Set up pre-commit hooks**:
    This is highly recommended as it will automatically run checks before you commit.
    ```bash
    pre-commit install
    ```

## Style Guides

### Git Commit Messages

This project uses [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/). Please follow this specification for your commit messages.

-   **feat**: A new feature.
-   **fix**: A bug fix.
-   **docs**: Documentation only changes.
-   **style**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc).
-   **refactor**: A code change that neither fixes a bug nor adds a feature.
-   **perf**: A code change that improves performance.
-   **test**: Adding missing tests or correcting existing tests.
-   **chore**: Changes to the build process or auxiliary tools and libraries such as documentation generation.

Example: `feat: Add 'safe squares' rule variant`

### Python Styleguide

-   Code is formatted with [Black](https://github.com/psf/black).
-   Linting is done with [Ruff](https://github.com/astral-sh/ruff).
-   Types are checked with [Mypy](http://mypy-lang.org/).

The pre-commit hooks will help enforce this, but you can also run the checks manually.

## Code Review Checklist

When you submit a pull request, reviewers will be looking for the following:

-   **Separation of Concerns**: Business logic should be in the `ludo/` package, not in the UI (`apps/`).
-   **Purity**: Functions that calculate game logic should be pure and free of side effects where possible.
-   **Test Coverage**: New features or bug fixes must be accompanied by tests.
-   **Documentation**: Public APIs, complex logic, and new features should be documented with docstrings and comments.
-   **Type Hinting**: All new code should be fully type-hinted.
