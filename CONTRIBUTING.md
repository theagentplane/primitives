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

## Change size

Small changes are easier to review, easier to revert and safer for the three repositories that
depend on this package.

- **Estimate before you start.** Count lines added plus lines removed. Do not count generated
  files (such as the schemas), lockfiles, or pure file moves and renames.
- **If the estimate is above 400 lines, consider splitting it.** Write a short plan: a list of
  logical components, each one reviewable on its own, passing CI, and ordered so that each builds
  on the one before. Put the plan in the issue or the pull request description, then open one pull
  request per component.
- **Split by logical component, not by size.** For example: the models, then schema generation,
  then the drift check. Not "the first half of the file".
- **Keeping it as one change is allowed** when it cannot be split sensibly, such as initial
  boilerplate, a mechanical change, or generated code. Say why in the pull request description.

This is a prompt to plan, not a hard limit. A workflow (`.github/workflows/pr-size.yml`) enforces
nothing: when a pull request is over 400 lines it adds the `size/large` label and one comment, and
removes them again if the pull request shrinks. It never fails and is not a required check.

## Proposing a schema change

Open an issue using the *Schema change proposal* template before writing code. Say which
consumers are affected and what each has to do to migrate.

## Commits and pull requests

- Write commit messages in the imperative ("Add Span model").
- Link the issue in the pull request description.
- CI must be green and CODEOWNERS review is required to merge.
