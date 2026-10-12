"""``LlmInput``: the input of an ``llm`` envelope (design sections 2.3 and 2.9).

Input is what the caller passed on this call: the requested model, the messages and the
instructions, tool definitions and sampling settings. ``raw`` holds the arguments exactly as
they were passed to the boundaried method, as JSON by argument name, and is always stored; the
canonical fields are derived from it.

``tools``, ``tool_choice`` and ``response_format`` are deliberately loose JSON: their shape
differs by provider and the design does not fix their structure, so this model accepts any JSON
there and does not check it. Making them stricter later would be a breaking change, so the
structure is a convention for the emitter (the Chronicle adapters) to follow, not a rule enforced
here. The exact provider value is always in ``raw``.

The convention, so every provider's input reads the same way:

- ``tools``: a list of ``{"name": str, "description": str (optional), "parameters": object
  (optional, a JSON Schema)}``.
- ``tool_choice``: ``"auto"``, ``"none"`` or ``"required"``, or ``{"name": str}`` to force one
  tool.
- ``response_format``: the provider's own object, unchanged (it varies too much to normalise).

If a stricter, enforced shape is ever needed, it should be a new optional field added in a minor
release, not a tightening of these.
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
        default=None,
        description="Tool definitions offered to the model. Not enforced; see the docstring.",
    )
    tool_choice: JsonValue = Field(
        default=None,
        description="Whether, or which, tool the model must use. Not enforced.",
    )
    response_format: dict[str, JsonValue] | None = Field(
        default=None,
        description="Requested answer format, as the provider expects it. Not checked.",
    )
    params: LlmParams = Field(default_factory=LlmParams)
    raw: dict[str, JsonValue] = Field(description="Arguments as passed, by name, as JSON.")
