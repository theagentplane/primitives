"""Tests for the id types."""

import pytest
from pydantic import TypeAdapter, ValidationError

from agentplane_primitives.types.id_types import EnvelopeId, SpanId, TraceId


@pytest.mark.parametrize(
    "bad",
    ["", "0" * 32, "A" * 32, "g" * 32, "a" * 31, "a" * 33, "a" * 32 + "\n", 12345, b"a" * 32],
)
def test_trace_id_rejects_bad_values(bad: object) -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(TraceId).validate_python(bad)


@pytest.mark.parametrize("adapter", [TypeAdapter(SpanId), TypeAdapter(EnvelopeId)])
@pytest.mark.parametrize("bad", ["0" * 16, "a" * 32, "ABCDEF0123456789", "a" * 15])
def test_short_ids_reject_bad_values(adapter: TypeAdapter[str], bad: str) -> None:
    with pytest.raises(ValidationError):
        adapter.validate_python(bad)


def test_ids_allow_zeros_inside() -> None:
    assert TypeAdapter(SpanId).validate_python("0000000000000001") == "0000000000000001"


def test_schema_says_what_the_pattern_cannot() -> None:
    # The all-zero rule is not expressible as a JSON Schema pattern, so it is in the description.
    schema = TypeAdapter(TraceId).json_schema()
    assert schema["pattern"] == "^[0-9a-f]{32}$"
    assert "not all zeros" in schema["description"]
