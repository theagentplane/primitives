"""``LlmParams``: the sampling settings the caller passed (design section 2.3).

Every field is optional: only what the caller set is recorded. Defaults baked into a client's
configuration are metadata, not input.
"""

from pydantic import Field

from agentplane_primitives.models.base import PrimitiveModel


class LlmParams(PrimitiveModel):
    """Sampling parameters passed on this call."""

    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = Field(default=None, ge=0)
    seed: int | None = None
    stop: list[str] | None = None
