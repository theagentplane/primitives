"""``ContentBlock``: one piece of LLM content (design sections 2.3 and 2.9).

A closed set chosen by ``type``: ``text``, ``tool_call``, ``reasoning`` or ``refusal``. Any other
``type`` is rejected. Each block has its own module.
"""

from typing import Annotated

from pydantic import Field

from agentplane_primitives.models.reasoning_block import ReasoningBlock
from agentplane_primitives.models.refusal_block import RefusalBlock
from agentplane_primitives.models.text_block import TextBlock
from agentplane_primitives.models.tool_call_block import ToolCallBlock

ContentBlock = Annotated[
    TextBlock | ToolCallBlock | ReasoningBlock | RefusalBlock,
    Field(discriminator="type"),
]
