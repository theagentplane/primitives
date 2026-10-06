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
