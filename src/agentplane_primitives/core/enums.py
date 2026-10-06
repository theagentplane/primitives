"""Closed sets of values shared by every entity (design section 2.9).

A new member of any enum here is a schema change: see ``docs/versioning.md``. Enums that only
exist inside one kind of payload (``finish_reason``, ``model_source``, content block types, message
roles) live with that payload.
"""

from enum import Enum


class Kind(str, Enum):
    """What an envelope records. Closed: there are no custom or unregistered kinds."""

    LLM = "llm"
    TOOL = "tool"


class State(str, Enum):
    """Lifecycle of a Trace, Span or Envelope. A closed record is immutable."""

    OPEN = "open"
    CLOSED = "closed"


class Status(str, Enum):
    """Result of a Span or Envelope (a Trace has none).

    A deliberate abort is a ``failure`` whose ``output.error.type`` is ``AbortCall``.
    """

    SUCCESS = "success"
    FAILURE = "failure"


class LinkType(str, Enum):
    """How one envelope relates to another besides parent and child.

    ``joined`` (fan-in) is reserved for future scope and is not a member yet.
    """

    RETRY_OF = "retry_of"
