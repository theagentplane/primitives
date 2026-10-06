"""Tests for the shared base model."""

import pytest
from pydantic import ValidationError

from agentplane_primitives.models import PrimitiveModel
from agentplane_primitives.types import SpanId


def test_unknown_fields_are_ignored_and_assignment_is_validated() -> None:
    class Sample(PrimitiveModel):
        span_id: SpanId

    sample = Sample.model_validate({"span_id": "a" * 16, "added_in_a_later_minor": 1})
    assert sample.model_dump() == {"span_id": "a" * 16}
    with pytest.raises(ValidationError):
        sample.span_id = "nope"
