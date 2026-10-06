"""``State``: where a Trace, Span or Envelope is in its lifecycle (design section 2.4).

Closed enum. A record is mutable while open and immutable once closed.
"""

from enum import Enum


class State(str, Enum):
    """Lifecycle state shared by Trace, Span and Envelope."""

    OPEN = "open"
    CLOSED = "closed"
