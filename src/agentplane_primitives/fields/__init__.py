"""Field types the entities are built from: closed enums, id types and metadata rules."""

from agentplane_primitives.fields.enums import Kind, LinkType, State, Status
from agentplane_primitives.fields.ids import (
    EnvelopeId,
    SpanId,
    TraceId,
    new_envelope_id,
    new_span_id,
    new_trace_id,
)
from agentplane_primitives.fields.metadata import (
    MESSAGE_ID,
    RESERVED_PREFIX,
    SESSION_ID,
    USER_ID,
    Metadata,
    MetadataKey,
    TraceMetadata,
    is_reserved_key,
)

__all__ = [
    "MESSAGE_ID",
    "RESERVED_PREFIX",
    "SESSION_ID",
    "USER_ID",
    "EnvelopeId",
    "Kind",
    "LinkType",
    "Metadata",
    "MetadataKey",
    "SpanId",
    "State",
    "Status",
    "TraceId",
    "TraceMetadata",
    "is_reserved_key",
    "new_envelope_id",
    "new_span_id",
    "new_trace_id",
]
