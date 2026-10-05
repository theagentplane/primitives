# agentplane-primitives

Shared, versioned **domain primitives** for the AgentPlane products: the entities that
[Chronicle](https://github.com/theagentplane/chronicle), the
[control plane](https://github.com/theagentplane/control-plane) and
[TokenOps](https://github.com/theagentplane/tokenops) all agree on.

> **Status: pre-alpha.** This release is the repository scaffold only. The models land in
> follow-up releases (see the [roadmap](#roadmap)).

## What belongs here

| In scope | Out of scope |
|---|---|
| The `Trace`, `Span` and `Envelope` entities and their payload variants | Storage, HTTP clients or servers |
| API request and response models | Business logic (pricing, policy, replay matching) |
| The `traceparent` carrier (parse and format) and id generation and validation | Visualization or export (OpenTelemetry mapping lives in the control plane) |
| Enumerations and well-known metadata keys | Anything that performs I/O |

The package depends on **pydantic only**. See [docs/design.md](docs/design.md) for how the
pieces fit together.

## Install

```bash
pip install agentplane-primitives
```

Requires Python 3.10+. The package is typed (PEP 561).

## Repository layout

```
src/agentplane_primitives/   the package (typed; version in _version.py)
tests/                       unit tests
schemas/                     generated JSON Schema, committed and drift-checked in CI
corpus/valid/, corpus/invalid/   golden payloads that every consumer validates against
docs/                        design notes and the versioning policy
.github/                     CI, release, dependency updates, templates
```

## Versioning

SemVer for the package, plus a `schema_version` on every payload. Additive changes only within
a major version. See [docs/versioning.md](docs/versioning.md).

## Development

Uses [uv](https://docs.astral.sh/uv/).

```bash
uv sync                          # create the environment with the dev group
uv run pytest                    # tests
uv run ruff check . && uv run ruff format --check .
uv run mypy                      # strict type check
uv build                         # sdist and wheel
```

See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Roadmap

1. Repository scaffold (this release).
2. `Trace`, `Span`, `Envelope`, the `llm` and `tool` payload variants, enums, ids.
3. The `traceparent` carrier and the API request and response models.
4. Committed JSON Schema, golden corpus, and the CI drift check.

## License

[MIT](LICENSE)
