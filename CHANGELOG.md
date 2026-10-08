# Changelog

All notable changes are recorded here, following [Keep a Changelog](https://keepachangelog.com/)
and [SemVer](https://semver.org/). Each entry is classified as **compatible** or **breaking** and
names the migration each consumer needs (see [docs/versioning.md](docs/versioning.md)).

## [Unreleased]

### Added
- Repository scaffold: `src` layout, typed package, tests, CI, release workflow, dependency
  updates, contribution and security docs. **Compatible** (no models yet).
- Foundations: the closed enums `Kind` (`llm`, `tool`), `State`, `Status` and `LinkType`; id
  types and generators for `trace_id`, `span_id` and `envelope_id`; the shared `PrimitiveModel`
  base (unknown fields ignored on read); and the metadata key and label conventions.
  **Compatible** (new API, nothing existed before). Consumers: nothing to migrate yet.
- Schema generation: `schema_files()` turns the public models into stable JSON Schema text,
  `scripts/generate_schemas.py` writes one file per model into `schemas/`, and a test fails when
  the committed files differ from the models. No model is public yet, so no schema file is
  committed. **Compatible** (new API and tooling only). Consumers: nothing to migrate.

### Changed
- Scope: HTTP request and response wrappers are not part of this package; the control plane owns
  them and reuses these entities as bodies (ADR 0003, Proposed). **Compatible** (documentation
  only; no model existed). The design document is updated to match.
