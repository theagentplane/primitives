# Releasing

Releases are published to PyPI by the `Release` workflow when a `v*` tag is pushed. It uses
PyPI Trusted Publishing (OIDC), so no API token is stored in the repository.

## One-time setup

1. On PyPI, add a **pending publisher** for the project `agentplane-primitives`:
   owner `theagentplane`, repository `primitives`, workflow `release.yml`, environment `pypi`.
2. In the GitHub repository settings, create an environment named `pypi`. Add required
   reviewers so a human approves each publish.

## Cutting a release

1. Bump `__version__` in `src/agentplane_primitives/_version.py`.
2. Move the `[Unreleased]` entries in `CHANGELOG.md` under the new version and date, each
   classified as compatible or breaking.
3. Merge that change to `main` through a pull request.
4. Tag and push: `git tag v<version> && git push origin v<version>`.
5. Approve the `pypi` environment deployment when prompted.

The workflow refuses to publish if the tag does not match `_version.py`.

## Version choice

Follow [docs/versioning.md](docs/versioning.md): a breaking change is a new major version, and
consumers upgrade before emitters when an enum gains a member.
