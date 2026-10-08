"""``State``: where a Trace, Span or Envelope is in its lifecycle (design section 2.4).

Closed enum. A record is mutable while open and immutable once closed.
"""

from agentplane_primitives.enums.base_enum import BaseEnum


class State(BaseEnum):
    """Lifecycle state shared by Trace, Span and Envelope."""

    OPEN = "open"
    CLOSED = "closed"
