"""``ToolOutput``: the output of a ``tool`` envelope (design section 2.3).

``raw`` is the JSON form of the return value. If the call failed, ``error`` says how (the
envelope's ``envelope_status.status`` carries only the high-level result).
"""

from pydantic import Field, JsonValue

from agentplane_primitives.models.base import PrimitiveModel
from agentplane_primitives.models.output_error import OutputError


class ToolOutput(PrimitiveModel):
    """What the tool returned, or the error it raised."""

    raw: JsonValue = Field(default=None, description="The return value, as JSON.")
    error: OutputError | None = None
