"""``LlmOutput``: the output of an ``llm`` envelope (design sections 2.3 and 2.9).

Output is what is known only from the response. It carries the fixed homes for cost data, which a
consumer such as TokenOps reads and nothing else:

- ``provider``: who served the call (``unknown`` when it cannot be determined)
- ``model`` and ``model_source``: what served it, and whether the response said so
- ``usage``: exclusive, additive token buckets

A call that failed has only ``error``; everything else is then absent. ``usage`` is null for a
custom boundary with no adapter, and consumers must tolerate that. ``raw`` is the value returned
by the boundaried method, as JSON, and is always stored.
"""

from pydantic import Field, JsonValue, model_validator

from agentplane_primitives.enums import FinishReason, ModelSource
from agentplane_primitives.models.base import PrimitiveModel
from agentplane_primitives.models.content_block import ContentBlock
from agentplane_primitives.models.output_error import OutputError
from agentplane_primitives.models.usage import Usage
from agentplane_primitives.types import UNKNOWN_PROVIDER, Provider


class LlmOutput(PrimitiveModel):
    """What came back from the model, or the error it raised."""

    content: list[ContentBlock] = Field(default_factory=list)
    finish_reason: FinishReason | None = None
    provider: Provider = UNKNOWN_PROVIDER
    model: str | None = Field(default=None, description="The model that served the call.")
    model_source: ModelSource | None = None
    usage: Usage | None = None
    response_id: str | None = None
    deployment_id: str | None = None
    raw: JsonValue = Field(default=None, description="The returned value, as JSON.")
    error: OutputError | None = None

    @model_validator(mode="after")
    def _model_and_source_go_together(self) -> "LlmOutput":
        if (self.model is None) != (self.model_source is None):
            raise ValueError("model and model_source must be given together")
        return self
