"""``Kind``: what an envelope records (design sections 2.3 and 2.9).

Closed enum: there are no custom or unregistered kinds, and any other value is rejected at
validation. A new kind is a schema change (see ``docs/versioning.md`` and ADR 0002).
"""

from agentplane_primitives.enums.base_enum import BaseEnum


class Kind(BaseEnum):
    """The kind of boundary crossing an envelope records. It selects the input and output shape."""

    LLM = "llm"
    TOOL = "tool"
