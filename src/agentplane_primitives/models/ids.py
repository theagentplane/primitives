"""Id types and their validation (design section 3.1).

Ids are lowercase hexadecimal and never all zero (W3C Trace Context treats an all-zero id as
invalid). ``trace_id`` is 128 bits (32 characters); ``span_id`` and ``envelope_id`` are 64 bits
(16 characters). Making new ids is in ``agentplane_primitives.utils.id_utils``.
"""

from typing import Annotated

from pydantic import AfterValidator, StringConstraints


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
