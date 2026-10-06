"""Small helper functions. No models live here; the traceparent helpers will join these."""

from agentplane_primitives.utils.id_utils import new_envelope_id, new_span_id, new_trace_id
from agentplane_primitives.utils.metadata_utils import is_reserved_key

__all__ = ["is_reserved_key", "new_envelope_id", "new_span_id", "new_trace_id"]
