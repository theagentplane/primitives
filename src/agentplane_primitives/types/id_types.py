"""Id types and their validation (design section 3.1).

Ids are lowercase hexadecimal and never all zero (W3C Trace Context treats an all-zero id as
invalid). ``trace_id`` is 128 bits (32 characters); ``span_id`` and ``envelope_id`` are 64 bits
(16 characters). Making new ids is in ``agentplane_primitives.utils.id_utils``.

The all-zero rule cannot be written as a JSON Schema pattern, so it is stated in each type's
description and enforced by the models only.
"""

from typing import Annotated

from pydantic import AfterValidator, Field, StringConstraints

TRACE_ID_LENGTH = 32
SHORT_ID_LENGTH = 16  # span_id and envelope_id


def _not_all_zero(value: str) -> str:
    # Length and hex digits are checked by the pattern on the type, which runs first.
    if value.strip("0") == "":
        raise ValueError("id must not be all zeros")
    return value


def _pattern(length: int) -> str:
    return f"^[0-9a-f]{{{length}}}$"


# The pattern also lands in the generated JSON Schema, so other languages can check ids too.
TraceId = Annotated[
    str,
    StringConstraints(strict=True, pattern=_pattern(TRACE_ID_LENGTH)),
    AfterValidator(_not_all_zero),
    Field(description="Trace id: 32 lowercase hex characters, not all zeros."),
]
SpanId = Annotated[
    str,
    StringConstraints(strict=True, pattern=_pattern(SHORT_ID_LENGTH)),
    AfterValidator(_not_all_zero),
    Field(description="Span id: 16 lowercase hex characters, not all zeros."),
]
EnvelopeId = Annotated[
    str,
    StringConstraints(strict=True, pattern=_pattern(SHORT_ID_LENGTH)),
    AfterValidator(_not_all_zero),
    Field(description="Envelope id: 16 lowercase hex characters, not all zeros."),
]
