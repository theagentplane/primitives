"""Small helper functions. No models live here; the traceparent helpers will join these."""

from agentplane_primitives.utils.ids import new_envelope_id, new_span_id, new_trace_id
from agentplane_primitives.utils.metadata import is_reserved_key

__all__ = ["is_reserved_key", "new_envelope_id", "new_span_id", "new_trace_id"]
