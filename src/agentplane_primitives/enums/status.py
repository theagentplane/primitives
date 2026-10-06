"""``Status``: the result of a Span or Envelope (design sections 2.2 and 2.9).

Closed enum. A Trace has no status of its own. There is no ``aborted`` value: a deliberate abort
is a ``failure`` whose ``output.error.type`` is ``AbortCall``.
"""

from enum import Enum


class Status(str, Enum):
    """High-level result of a Span or Envelope."""

    SUCCESS = "success"
    FAILURE = "failure"
