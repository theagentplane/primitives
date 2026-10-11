"""Field types the models are built from: ids, metadata, schema version and provider."""

from agentplane_primitives.types.id_types import EnvelopeId, SpanId, TraceId
from agentplane_primitives.types.metadata_types import (
    MESSAGE_ID,
    RESERVED_PREFIX,
    SESSION_ID,
    USER_ID,
    Metadata,
    MetadataKey,
    TraceMetadata,
)
from agentplane_primitives.types.provider_types import (
    UNKNOWN_PROVIDER,
    WELL_KNOWN_PROVIDERS,
    Provider,
)
from agentplane_primitives.types.schema_version_types import SCHEMA_VERSION, SchemaVersion

__all__ = [
    "MESSAGE_ID",
    "RESERVED_PREFIX",
    "SCHEMA_VERSION",
    "SESSION_ID",
    "UNKNOWN_PROVIDER",
    "USER_ID",
    "WELL_KNOWN_PROVIDERS",
    "EnvelopeId",
    "Metadata",
    "MetadataKey",
    "Provider",
    "SchemaVersion",
    "SpanId",
    "TraceId",
    "TraceMetadata",
]
