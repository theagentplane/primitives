"""``Provider``: who served an LLM call (design section 2.9).

An open set: any string is accepted, and the well-known names below are the ones consumers can
rely on. ``unknown`` means it could not be determined (a custom boundary with no adapter).
"""

from typing import Annotated

from pydantic import Field, StringConstraints

UNKNOWN_PROVIDER = "unknown"
WELL_KNOWN_PROVIDERS = ("openai", "anthropic", "azure", "google", "bedrock", "litellm")

Provider = Annotated[
    str,
    StringConstraints(strict=True, min_length=1),
    Field(description="Who served the call, e.g. openai, or unknown."),
]
