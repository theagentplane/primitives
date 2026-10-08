"""``LinkType``: how one envelope relates to another besides parent and child (design 2.5).

Closed enum for now. ``joined`` (fan-in) is reserved for future scope and is not a member yet.
"""

from agentplane_primitives.enums.base_enum import BaseEnum


class LinkType(BaseEnum):
    """The relationship a link expresses."""

    RETRY_OF = "retry_of"
