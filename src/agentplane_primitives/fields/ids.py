"""Id types, generation and validation (design section 3.1).

Ids are lowercase hexadecimal, random, and never all zero (W3C Trace Context treats an all-zero
id as invalid). ``trace_id`` is 128 bits (32 characters); ``span_id`` and ``envelope_id`` are 64
bits (16 characters). Generation uses the operating system's random source, not ``random``.
"""

import secrets
from typing import Annotated

from pydantic import AfterValidator, StringConstraints

_TRACE_ID_LENGTH = 32
_SHORT_ID_LENGTH = 16


def _not_all_zero(value: str) -> str:
    # Length and hex digits are checked by the pattern on the type, which runs first.
    if value.strip("0") == "":
        raise ValueError("id must not be all zeros")
    return value


# The pattern also lands in the generated JSON Schema, so other languages can check ids too.
TraceId = Annotated[
    str,
    StringConstraints(strict=True, pattern=r"^[0-9a-f]{32}$"),
    AfterValidator(_not_all_zero),
]
SpanId = Annotated[
    str,
    StringConstraints(strict=True, pattern=r"^[0-9a-f]{16}$"),
    AfterValidator(_not_all_zero),
]
EnvelopeId = Annotated[
    str,
    StringConstraints(strict=True, pattern=r"^[0-9a-f]{16}$"),
    AfterValidator(_not_all_zero),
]


def _random_hex(length: int) -> str:
    while True:  # an all-zero draw is astronomically unlikely, but it would be invalid
        value = secrets.token_hex(length // 2)
        if value.strip("0"):
            return value


def new_trace_id() -> str:
    """Return a new random ``trace_id``."""
    return _random_hex(_TRACE_ID_LENGTH)


def new_span_id() -> str:
    """Return a new random ``span_id``."""
    return _random_hex(_SHORT_ID_LENGTH)


def new_envelope_id() -> str:
    """Return a new random ``envelope_id``."""
    return _random_hex(_SHORT_ID_LENGTH)
