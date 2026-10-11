"""``ReasoningBlock``: the model's visible reasoning text (design section 2.3)."""

from typing import Literal

from agentplane_primitives.models.base import PrimitiveModel


class ReasoningBlock(PrimitiveModel):
    """Reasoning content returned by the model."""

    type: Literal["reasoning"] = "reasoning"
    text: str
