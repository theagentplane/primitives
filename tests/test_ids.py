"""Tests for the id types and generators."""

from collections.abc import Callable

import pytest
from pydantic import TypeAdapter, ValidationError

from agentplane_primitives.models.ids import (
    EnvelopeId,
    SpanId,
    TraceId,
    new_envelope_id,
    new_span_id,
    new_trace_id,
)


@pytest.mark.parametrize(
    ("adapter", "make", "length"),
    [
        (TypeAdapter(TraceId), new_trace_id, 32),
        (TypeAdapter(SpanId), new_span_id, 16),
        (TypeAdapter(EnvelopeId), new_envelope_id, 16),
    ],
)
def test_generated_ids_are_valid_and_random(
    adapter: TypeAdapter[str], make: Callable[[], str], length: int
) -> None:
    ids = {make() for _ in range(50)}
    assert len(ids) == 50
    for value in ids:
        assert len(value) == length
        assert adapter.validate_python(value) == value


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
