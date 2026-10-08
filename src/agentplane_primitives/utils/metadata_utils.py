"""Helpers for the metadata key conventions (design section 2.9).

The key and label types themselves are in ``agentplane_primitives.types.metadata_types``.
"""

from agentplane_primitives.types.metadata_types import RESERVED_PREFIX


def is_reserved_key(key: str) -> bool:
    """Return True if ``key`` uses the prefix reserved for Chronicle itself."""
    return key.startswith(RESERVED_PREFIX)
