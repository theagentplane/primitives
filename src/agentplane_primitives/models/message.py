"""``Message``: one message in an LLM input (design sections 2.3 and 2.9).

``content`` is plain text or a list of content blocks. A ``tool`` message (a tool result being
handed back to the model) names the call it answers in ``tool_call_id``: the ``id`` of the
``ToolCallBlock`` the model produced, copied from the provider's own id (OpenAI ``tool_call_id``,
Anthropic ``tool_use_id``, Bedrock ``toolUseId``). Not every provider sends one, so it is
optional, and it is not checked against earlier messages. Anthropic carries a tool result as a
``tool_result`` block inside a user message; an adapter maps that to a ``tool`` message here. The
provider's exact message shape is kept in ``input.raw``.
"""

from pydantic import Field

from agentplane_primitives.enums import MessageRole
from agentplane_primitives.models.base import PrimitiveModel
from agentplane_primitives.models.content_block import ContentBlock


class Message(PrimitiveModel):
    """A single message with a role."""

    role: MessageRole
    content: str | list[ContentBlock]
    tool_call_id: str | None = Field(
        default=None, description="For role=tool: the id of the tool call this answers."
    )
