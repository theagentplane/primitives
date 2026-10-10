"""``ModelSource``: where ``output.model`` came from (design sections 2.3 and 2.9).

Closed enum. Some SDKs do not return the served model; then the adapter copies the requested one
and says so here, so a consumer knows how much to trust it.
"""

from agentplane_primitives.enums.base_enum import BaseEnum


class ModelSource(BaseEnum):
    """How the model name in the output was obtained."""

    SERVED = "served"
    """The response named the model that served the call."""

    REQUESTED = "requested"
    """The response had no model; the adapter copied the requested one."""
