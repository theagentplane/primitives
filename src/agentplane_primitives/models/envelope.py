"""``Envelope``: one boundary crossing, as a single record (design sections 2.2 to 2.5).

The fields fall into the five sections of the design. The identity fields sit at the top level,
as in the design's example payloads; the other four sections are nested:

- identity: ``envelope_id``, ``span_id``, ``trace_id``, ``parent_envelope_id``, ``name``,
  ``kind``, ``attempt``, ``links``
- ``envelope_status``, ``input``, ``output`` and ``metadata``

``kind`` selects the shape of ``input`` and ``output``: ``tool`` uses ``ToolInput`` and
``ToolOutput``, ``llm`` uses ``LlmInput`` and ``LlmOutput``. A payload of the other kind's shape
is rejected. An envelope is open until closed; a closed envelope must have an ``output`` (an
error is recorded there).
"""

from typing import Any

from pydantic import BaseModel, Field, model_validator

from agentplane_primitives.enums import Kind, State
from agentplane_primitives.models.base import PrimitiveModel
from agentplane_primitives.models.envelope_status import EnvelopeStatus
from agentplane_primitives.models.link import Link
from agentplane_primitives.models.llm_input import LlmInput
from agentplane_primitives.models.llm_output import LlmOutput
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

_PAYLOADS: dict[Kind, tuple[type[BaseModel], type[BaseModel]]] = {
    Kind.TOOL: (ToolInput, ToolOutput),
    Kind.LLM: (LlmInput, LlmOutput),
}


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
    input: ToolInput | LlmInput = Field(description="Shape chosen by kind: tool or llm input.")
    output: ToolOutput | LlmOutput | None = Field(
        default=None, description="Shape chosen by kind: tool or llm output."
    )
    metadata: Metadata = Field(default_factory=dict)

    @model_validator(mode="before")
    @classmethod
    def _read_payloads_by_kind(cls, data: Any) -> Any:
        # The two payload shapes overlap when unknown fields are ignored, so the kind, not the
        # shape, decides which model reads input and output.
        if not isinstance(data, dict):
            return data
        try:
            input_model, output_model = _PAYLOADS[Kind(data.get("kind"))]
        except ValueError:
            return data  # an unknown kind is reported by the kind field itself
        data = dict(data)
        if isinstance(data.get("input"), dict):
            data["input"] = input_model.model_validate(data["input"])
        if isinstance(data.get("output"), dict):
            data["output"] = output_model.model_validate(data["output"])
        return data

    @model_validator(mode="after")
    def _check_consistency(self) -> "Envelope":
        input_model, output_model = _PAYLOADS[self.kind]
        if not isinstance(self.input, input_model):
            raise ValueError(f"input does not match kind {self.kind.value!r}")
        if self.output is not None and not isinstance(self.output, output_model):
            raise ValueError(f"output does not match kind {self.kind.value!r}")
        if self.envelope_status.state is State.CLOSED and self.output is None:
            raise ValueError("a closed envelope needs an output")
        return self
