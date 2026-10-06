"""Tests for the id types."""

import pytest
from pydantic import TypeAdapter, ValidationError

from agentplane_primitives.models.ids import EnvelopeId, SpanId, TraceId


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
