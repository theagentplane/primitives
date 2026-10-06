"""Base class, id types and metadata rules that the entities are built from."""

from agentplane_primitives.models.base import PrimitiveModel
from agentplane_primitives.models.ids import EnvelopeId, SpanId, TraceId
from agentplane_primitives.models.metadata import (
    MESSAGE_ID,
    RESERVED_PREFIX,
    SESSION_ID,
    USER_ID,
    Metadata,
    MetadataKey,
    TraceMetadata,
)

__all__ = [
    "MESSAGE_ID",
    "RESERVED_PREFIX",
    "SESSION_ID",
    "USER_ID",
    "EnvelopeId",
    "Metadata",
    "MetadataKey",
    "PrimitiveModel",
    "SpanId",
    "TraceId",
    "TraceMetadata",
]
