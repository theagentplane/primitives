"""``MessageRole``: who a message in an LLM input is from (design section 2.9). Closed enum."""

from agentplane_primitives.enums.base_enum import BaseEnum


class MessageRole(BaseEnum):
    """The author of a message."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
