"""``Envelope``: one boundary crossing, as a single record (design sections 2.2 to 2.5).

The fields fall into the five sections of the design. The identity fields sit at the top level,
as in the design's example payloads; the other four sections are nested:

- identity: ``envelope_id``, ``span_id``, ``trace_id``, ``parent_envelope_id``, ``name``,
  ``kind``, ``attempt``, ``links``
- ``envelope_status``, ``input``, ``output`` and ``metadata``

``kind`` selects the shape of ``input`` and ``output``. Only ``tool`` has a shape so far; ``llm``
is rejected until its models land. An envelope is open until closed; a closed envelope must have
an ``output`` (an error is recorded there).
"""

from pydantic import Field, model_validator

from agentplane_primitives.enums import Kind, State
from agentplane_primitives.models.base import PrimitiveModel
from agentplane_primitives.models.envelope_status import EnvelopeStatus
from agentplane_primitives.models.link import Link
from agentplane_primitives.models.tool_input import ToolInput
from agentplane_primitives.models.tool_output import ToolOutput
from agentplane_primitives.types import (
    SCHEMA_VERSION,
    EnvelopeId,
    Metadata,
    SchemaVersion,
    SpanId,
    TraceId,
)


class Envelope(PrimitiveModel):
    """The record of one call across a boundary inside a span."""

    schema_version: SchemaVersion = SCHEMA_VERSION

    # identity
    envelope_id: EnvelopeId
    span_id: SpanId
    trace_id: TraceId
    parent_envelope_id: EnvelopeId | None = None
    name: str = Field(min_length=1, description="Boundary name, e.g. agent.chat.")
    kind: Kind
    attempt: int = Field(default=1, ge=1, description="1 for the first try, 2 for a retry, ...")
    links: list[Link] = Field(default_factory=list)

    envelope_status: EnvelopeStatus
    input: ToolInput
    output: ToolOutput | None = None
    metadata: Metadata = Field(default_factory=dict)

    @model_validator(mode="after")
    def _check_consistency(self) -> "Envelope":
        if self.kind is not Kind.TOOL:
            raise ValueError(f"kind {self.kind.value!r} has no input and output models yet")
        if self.envelope_status.state is State.CLOSED and self.output is None:
            raise ValueError("a closed envelope needs an output")
        return self
