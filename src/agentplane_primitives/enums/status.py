"""``Status``: the result of a Span or Envelope (design sections 2.2 and 2.9).

Closed enum. A Trace has no status of its own. There is no ``aborted`` value: a deliberate abort
is a ``failure`` whose ``output.error.type`` is ``AbortCall``.
"""

from agentplane_primitives.enums.base_enum import BaseEnum


class Status(BaseEnum):
    """High-level result of a Span or Envelope."""

    SUCCESS = "success"
    FAILURE = "failure"
