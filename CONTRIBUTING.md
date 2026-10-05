# Contributing

Three repositories depend on this package, so changes here are reviewed more carefully than
usual. Keep pull requests small and focused on one thing.

## Setup

Uses [uv](https://docs.astral.sh/uv/) and Python 3.10 or newer.

```bash
git clone https://github.com/theagentplane/primitives.git
cd primitives
uv sync                  # creates the environment with the dev group
uv run pre-commit install    # optional: run the checks on every commit
```

## Checks (CI runs the same ones)

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest --cov
uv build && uv run twine check dist/*
```

## Ground rules

- **No I/O, no business logic.** This package defines data and validation only. Storage,
  HTTP, pricing and replay logic belong in the consumers.
- **Dependencies:** pydantic only. A new runtime dependency needs a strong reason and a
  discussion first.
- **Every model change needs:** tests, the regenerated schemas (`src/agentplane_primitives/schemas/`), and a CHANGELOG
  entry classified as compatible or breaking.
- **Compatibility:** follow [docs/versioning.md](docs/versioning.md). Additive changes only
  within a major version. A new enum member is a schema change.
- **Public API is typed.** `mypy --strict` must pass.

## Proposing a schema change

Open an issue using the *Schema change proposal* template before writing code. Say which
consumers are affected and what each has to do to migrate.

## Commits and pull requests

- Write commit messages in the imperative ("Add Span model").
- Link the issue in the pull request description.
- CI must be green and CODEOWNERS review is required to merge.
