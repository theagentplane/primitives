"""``FinishReason``: why an LLM call stopped (design section 2.9).

Closed enum of the canonical set. The provider's own original value stays in ``output.raw``, so
nothing is lost when a provider value is mapped onto one of these.
"""

from agentplane_primitives.enums.base_enum import BaseEnum


class FinishReason(BaseEnum):
    """The canonical reason an LLM response ended."""

    STOP = "stop"
    LENGTH = "length"
    TOOL_CALLS = "tool_calls"
    CONTENT_FILTER = "content_filter"
    OTHER = "other"
