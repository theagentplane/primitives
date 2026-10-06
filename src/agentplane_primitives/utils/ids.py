"""Generate new ids (design section 3.1).

Ids are random, never all zero, and come from the operating system's random source
(``secrets``), not ``random``. The matching types that validate them are in
``agentplane_primitives.models.ids``.
"""

import secrets

_TRACE_ID_LENGTH = 32
_SHORT_ID_LENGTH = 16


def _random_hex(length: int) -> str:
    while True:  # an all-zero draw is astronomically unlikely, but it would be invalid
        value = secrets.token_hex(length // 2)
        if value.strip("0"):
            return value


def new_trace_id() -> str:
    """Return a new random ``trace_id``: 32 lowercase hex characters."""
    return _random_hex(_TRACE_ID_LENGTH)


def new_span_id() -> str:
    """Return a new random ``span_id``: 16 lowercase hex characters."""
    return _random_hex(_SHORT_ID_LENGTH)


def new_envelope_id() -> str:
    """Return a new random ``envelope_id``: 16 lowercase hex characters."""
    return _random_hex(_SHORT_ID_LENGTH)
