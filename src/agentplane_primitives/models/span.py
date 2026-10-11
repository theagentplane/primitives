"""``Span``: one service's handling of a request (design sections 2.1 and 2.2).

A Span sits between the Trace and its Envelopes: one process, one agent run. It is minted by its
own service, so ``span_id`` is unique within the trace. ``parent_envelope_id`` is the envelope in
the caller's span that made the outbound call; it is the only link between services, and it is
empty for the first span in a trace.

``status`` is ``success`` or ``failure`` and is set when the span closes, by the entry point:
``failure`` if the request handler raised, otherwise ``success``. It is independent of envelope
failures (a retry that was handled does not fail the span). Like an envelope, a span is open until
closed; to close one, build a new ``Span``, because the fields are validated together.
"""

from pydantic import AwareDatetime, Field, model_validator

from agentplane_primitives.enums import State, Status
from agentplane_primitives.models.base import PrimitiveModel
from agentplane_primitives.types import (
    SCHEMA_VERSION,
    EnvelopeId,
    Metadata,
    SchemaVersion,
    SpanId,
    TraceId,
)
from agentplane_primitives.utils.lifecycle_utils import validate_state_status_and_times


class Span(PrimitiveModel):
    """One service's handling of a request inside a trace. Times must carry a time zone."""

    schema_version: SchemaVersion = SCHEMA_VERSION
    span_id: SpanId
    trace_id: TraceId
    parent_envelope_id: EnvelopeId | None = None
    service: str = Field(min_length=1, description="Service or agent name.")
    state: State
    status: Status | None = None
    started_at: AwareDatetime
    ended_at: AwareDatetime | None = None
    metadata: Metadata = Field(default_factory=dict, description="Span-level setup.")

    @model_validator(mode="after")
    def _validate_state_fields(self) -> "Span":
        validate_state_status_and_times(
            self.state, self.status, self.started_at, self.ended_at, "span"
        )
        return self
