"""``Usage``: token counts for one LLM call, in fixed buckets (design sections 2.3 and 2.9).

The buckets are exclusive and additive, and the same for every provider: the total is their sum
and each bucket is priced once. Providers disagree on conventions (OpenAI counts cached tokens
inside the input total, Anthropic counts them separately), so the adapter converts them into
these buckets and the consumer does not have to.
"""

from pydantic import Field

from agentplane_primitives.models.base import PrimitiveModel


class Usage(PrimitiveModel):
    """Token counts. A bucket the provider did not report is 0."""

    input: int = Field(default=0, ge=0, description="Non-cached input tokens.")
    cached_read: int = Field(default=0, ge=0, description="Input tokens read from the cache.")
    cache_write: int = Field(default=0, ge=0, description="Tokens written to the cache.")
    output: int = Field(default=0, ge=0, description="Non-reasoning output tokens.")
    reasoning: int = Field(default=0, ge=0, description="Reasoning output tokens.")
