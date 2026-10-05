# Versioning policy

Three repositories depend on this package, so compatibility is a contract and not a courtesy.

## Two versions

- **Package version** follows [SemVer](https://semver.org/) (`major.minor.patch`).
- **`schema_version`** (`major.minor`) is carried on every persisted payload. The package major
  equals the schema major.

## Rules

- **Additive-only within a major.**
  - New optional fields are allowed. Readers ignore fields they do not know.
  - New members of a closed enum, including a new envelope `kind`, are additive for the writer.
    A reader on an older minor rejects the unknown value, so **consumers upgrade before emitters**.
- **A breaking change is a new major.** The control plane accepts the current and the previous
  major on ingest and upconverts on read.
- **Release order for a breaking change:** primitives, then the control plane (reads both
  majors), then Chronicle and TokenOps (emit the new one).
- **Pre-1.0:** consumers pin the exact minor (`==0.y.*`). From 1.0: `>=1.2,<2`.
- **Deprecation:** a field or enum value is deprecated for at least one minor before removal,
  and the changelog says so.

## Safety nets

- **One source of truth:** consumers import these models instead of writing their own parsers,
  so they validate against the same code. (A shared set of example payloads for consumers that
  parse by hand can be added later if one appears.)
- **Committed JSON Schema** (`src/agentplane_primitives/schemas/`): generated from the models. CI fails if the committed
  files differ from what the models generate.

## Changelog

Every change is classified in [CHANGELOG.md](../CHANGELOG.md) as compatible or breaking, and
names the migration each consumer needs.
