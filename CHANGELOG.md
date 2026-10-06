# Changelog

All notable changes are recorded here, following [Keep a Changelog](https://keepachangelog.com/)
and [SemVer](https://semver.org/). Each entry is classified as **compatible** or **breaking** and
names the migration each consumer needs (see [docs/versioning.md](docs/versioning.md)).

## [Unreleased]

### Added
- Repository scaffold: `src` layout, typed package, tests, CI, release workflow, dependency
  updates, contribution and security docs. **Compatible** (no models yet).

### Changed
- Scope: HTTP request and response wrappers are not part of this package; the control plane owns
  them and reuses these entities as bodies (ADR 0003, Proposed). **Compatible** (documentation
  only; no model existed). The design document is updated to match.
