"""``LlmInput``: the input of an ``llm`` envelope (design sections 2.3 and 2.9).

Input is what the caller passed on this call: the requested model, the messages and the
instructions, tool definitions and sampling settings. ``raw`` holds the arguments exactly as
they were passed to the boundaried method, as JSON by argument name, and is always stored; the
canonical fields are derived from it.

``tools``, ``tool_choice`` and ``response_format`` are kept as JSON objects because their shape
differs by provider. The design does not fix their structure.
"""

from pydantic import Field, JsonValue

from agentplane_primitives.models.base import PrimitiveModel
from agentplane_primitives.models.llm_params import LlmParams
from agentplane_primitives.models.message import Message


class LlmInput(PrimitiveModel):
    """What was sent to the model."""

    model: str = Field(min_length=1, description="The model or alias the caller asked for.")
    messages: list[Message]
    system: str | None = Field(default=None, description="Instructions the caller supplied.")
    tools: list[dict[str, JsonValue]] | None = Field(
        default=None, description="Tool definitions offered to the model."
    )
    tool_choice: JsonValue = Field(
        default=None, description="Whether, or which, tool the model must use."
    )
    response_format: dict[str, JsonValue] | None = None
    params: LlmParams = Field(default_factory=LlmParams)
    raw: dict[str, JsonValue] = Field(description="Arguments as passed, by name, as JSON.")
