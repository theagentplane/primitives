"""Building blocks shared by every entity: base model, enums, ids and metadata conventions."""

from agentplane_primitives.core.base import PrimitiveModel
from agentplane_primitives.core.enums import Kind, LinkType, State, Status
from agentplane_primitives.core.ids import (
    EnvelopeId,
    SpanId,
    TraceId,
    new_envelope_id,
    new_span_id,
    new_trace_id,
)
from agentplane_primitives.core.metadata import (
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
    "PrimitiveModel",
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
