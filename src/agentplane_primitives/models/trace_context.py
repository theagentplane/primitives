"""``TraceContext``: what travels between services in the ``traceparent`` header (design 3.2).

It is a carrier, not a stored entity, so it has no JSON Schema file. A service that receives a
valid ``traceparent`` joins that trace and opens a new Span whose ``parent_envelope_id`` is the
received id. The ``parent-id`` field of the W3C header carries the caller's outbound-call
envelope id; the parent span id is not passed, because the control plane resolves an envelope to
its span.

Reading and writing the header is in ``agentplane_primitives.utils.traceparent_utils``.
"""

from pydantic import Field

from agentplane_primitives.models.base import PrimitiveModel
from agentplane_primitives.types import EnvelopeId, TraceId


class TraceContext(PrimitiveModel):
    """The trace a request belongs to and the envelope that made the call."""

    trace_id: TraceId
    parent_envelope_id: EnvelopeId = Field(
        description="The caller's outbound-call envelope, sent as the W3C parent-id."
    )
    flags: str = Field(
        default="01",
        pattern=r"^[0-9a-f]{2}$",
        description="W3C trace-flags byte as two lowercase hex characters (01 = sampled).",
    )
