"""``ToolCallBlock``: the model asking for a tool to be called (design section 2.3)."""

from typing import Literal

from pydantic import Field, JsonValue

from agentplane_primitives.models.base import PrimitiveModel


class ToolCallBlock(PrimitiveModel):
    """A request from the model to call a tool, with parsed arguments."""

    type: Literal["tool_call"] = "tool_call"
    id: str | None = Field(default=None, description="The provider's id for this call, if any.")
    name: str = Field(min_length=1)
    arguments: dict[str, JsonValue] = Field(default_factory=dict)
