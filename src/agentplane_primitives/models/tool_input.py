"""``ToolInput``: the input of a ``tool`` envelope (design section 2.3).

For a tool the canonical view is the raw data itself, so it is stored once, as the arguments
bound by name.
"""

from pydantic import Field, JsonValue

from agentplane_primitives.models.base import PrimitiveModel


class ToolInput(PrimitiveModel):
    """The arguments the tool was called with, in JSON form."""

    raw: dict[str, JsonValue] = Field(description="Bound arguments by name, as JSON.")
