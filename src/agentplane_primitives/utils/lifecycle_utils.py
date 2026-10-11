"""The open and closed rule shared by the envelope status and the Span (design section 2.4).

A record is mutable until it is closed. While ``open`` it has a start time and nothing else; once
``closed`` it has a result (``status``) and an end time. The Trace follows the open and closed
states too but has no status of its own, so it does not use this check.
"""

from datetime import datetime

from agentplane_primitives.enums import State, Status


def validate_state_status_and_times(
    state: State,
    status: Status | None,
    started_at: datetime,
    ended_at: datetime | None,
    what: str,
) -> None:
    """Raise ``ValueError`` unless ``status`` and ``ended_at`` agree with ``state``.

    An ``open`` record must have neither; a ``closed`` one must have both, with ``ended_at`` not
    before ``started_at``.

    ``what`` names the record in the error message, for example ``"envelope"`` or ``"span"``.
    """
    if state is State.OPEN:
        if status is not None or ended_at is not None:
            raise ValueError(f"an open {what} has no status and no ended_at yet")
    elif status is None or ended_at is None:
        raise ValueError(f"a closed {what} needs a status and an ended_at")
    elif ended_at < started_at:
        raise ValueError("ended_at must not be before started_at")
