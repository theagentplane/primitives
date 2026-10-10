"""``OutputError``: how a failed call is described inside an output (design sections 2.3, 2.9).

Error information belongs to ``output``, not to metadata. ``type`` is the exception class name; the
reserved value ``"AbortCall"`` means a hook stopped the call on purpose.
"""

from pydantic import Field

from agentplane_primitives.models.base import PrimitiveModel

ABORT_CALL = "AbortCall"


class OutputError(PrimitiveModel):
    """An error raised by the call, recorded in ``output.error``."""

    type: str = Field(min_length=1, description="Exception class name, e.g. RateLimitError.")
    message: str = Field(description="The exception message.")
