"""Metadata conventions for all entities (design sections 2.6 and 2.9).

- Keys are lowercase and dot-separated, for example ``client.library``.
- The ``chronicle.`` prefix is reserved for keys Chronicle itself sets. The models accept those
  keys (they carry what Chronicle wrote); keeping user code off the prefix is the SDK's job, and
  ``agentplane_primitives.utils.metadata_utils.is_reserved_key`` is there for it.
- Trace labels have string values, because they are indexed and filtered on. Span and Envelope
  metadata values may be any JSON value.
"""

from typing import Annotated

from pydantic import JsonValue, StringConstraints

RESERVED_PREFIX = "chronicle."

# Well-known Trace label keys (documented, not fields on the entity).
SESSION_ID = "session_id"
MESSAGE_ID = "message_id"
USER_ID = "user_id"

MetadataKey = Annotated[
    str,
    StringConstraints(strict=True, pattern=r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$"),
]

TraceMetadata = dict[MetadataKey, str]
"""Trace labels: written once, string values only."""

Metadata = dict[MetadataKey, JsonValue]
"""Span and Envelope metadata: any JSON value."""
