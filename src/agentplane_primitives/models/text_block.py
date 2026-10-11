"""``TextBlock``: plain text produced or sent in an LLM call (design section 2.3)."""

from typing import Literal

from agentplane_primitives.models.base import PrimitiveModel


class TextBlock(PrimitiveModel):
    """A piece of text."""

    type: Literal["text"] = "text"
    text: str
