"""Read and write the W3C ``traceparent`` header (design section 3.2).

The header is ``00-<trace_id>-<parent-id>-<flags>``: version ``00``, a 32 character trace id, a
16 character parent id and a two character flags byte, all lowercase hex, joined by dashes. In
Chronicle the parent id is the caller's outbound-call envelope id.

``parse_traceparent`` reads a value that arrives from the network, so it never raises: anything
it does not accept gives ``None``, and the caller then mints a new trace instead of joining. It
is strict on purpose: only version ``00``, exactly the layout above, lowercase hex, no
surrounding whitespace, and no all-zero trace id or parent id (the W3C spec rejects those).

``to_event`` and ``from_event`` are reserved for carrying a trace context through queues and
webhooks (design section 3.4, future scope). The names exist so nothing else takes them; they
are documented and not implemented.
"""

import re

from pydantic import ValidationError

from agentplane_primitives.models.trace_context import TraceContext
from agentplane_primitives.types.id_types import SHORT_ID_LENGTH, TRACE_ID_LENGTH

_VERSION = "00"
_HEADER = re.compile(
    rf"{_VERSION}-(?P<trace_id>[0-9a-f]{{{TRACE_ID_LENGTH}}})"
    rf"-(?P<parent>[0-9a-f]{{{SHORT_ID_LENGTH}}})-(?P<flags>[0-9a-f]{{2}})"
)


def parse_traceparent(header: object) -> TraceContext | None:
    """Return the trace context in ``header``, or ``None`` if it is missing or not valid.

    Never raises: ``header`` may be ``None``, not a string, or arbitrary text from the network.
    """
    if not isinstance(header, str):
        return None
    match = _HEADER.fullmatch(header)
    if match is None:
        return None
    try:
        return TraceContext(
            trace_id=match["trace_id"],
            parent_envelope_id=match["parent"],
            flags=match["flags"],
        )
    except ValidationError:  # an all-zero id matches the layout but is not valid
        return None


def format_traceparent(context: TraceContext) -> str:
    """Return the ``traceparent`` header value for ``context``."""
    return f"{_VERSION}-{context.trace_id}-{context.parent_envelope_id}-{context.flags}"


def to_event(context: TraceContext) -> dict[str, str]:
    """Reserved: carry ``context`` in a queue message or webhook. Not implemented."""
    raise NotImplementedError("to_event is reserved for future scope (design section 3.4)")


def from_event(event: dict[str, str]) -> TraceContext | None:
    """Reserved: read a trace context from a queue message or webhook. Not implemented."""
    raise NotImplementedError("from_event is reserved for future scope (design section 3.4)")
