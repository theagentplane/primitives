"""Tests for the id generators."""

import secrets
from collections.abc import Callable

import pytest
from pydantic import TypeAdapter

from agentplane_primitives.types import EnvelopeId, SpanId, TraceId
from agentplane_primitives.utils import new_envelope_id, new_span_id, new_trace_id


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


def test_all_zero_draw_is_redrawn(monkeypatch: pytest.MonkeyPatch) -> None:
    draws = iter(["0" * 16, "0000000000000007"])
    monkeypatch.setattr(secrets, "token_hex", lambda _nbytes: next(draws))
    assert new_span_id() == "0000000000000007"
