"""``SchemaVersion``: the ``major.minor`` version carried on every persisted payload (design 2.8).

The package major equals the schema major. Before 1.0 the schema version tracks the package
minor, so package ``0.1.x`` writes schema ``"0.1"``. Policy: ``docs/versioning.md``.
"""

from typing import Annotated

from pydantic import Field, StringConstraints

SCHEMA_VERSION = "0.1"
"""The schema version this release of the package writes."""

SchemaVersion = Annotated[
    str,
    StringConstraints(strict=True, pattern=r"^[0-9]+\.[0-9]+$"),
    Field(description="Schema version, major.minor."),
]
