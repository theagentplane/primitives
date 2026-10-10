"""``RefusalBlock``: the model declining to answer (design section 2.3)."""

from typing import Literal

from agentplane_primitives.models.base import PrimitiveModel


class RefusalBlock(PrimitiveModel):
    """A refusal returned by the model."""

    type: Literal["refusal"] = "refusal"
    text: str
