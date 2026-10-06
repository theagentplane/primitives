"""Tests for enums, ids, the base model and metadata conventions."""

from collections.abc import Callable

import pytest
from pydantic import TypeAdapter, ValidationError

from agentplane_primitives.base import PrimitiveModel
from agentplane_primitives.enums import Kind, LinkType, State, Status
from agentplane_primitives.ids import (
    EnvelopeId,
    SpanId,
    TraceId,
    new_envelope_id,
    new_span_id,
    new_trace_id,
)
from agentplane_primitives.metadata import Metadata, TraceMetadata, is_reserved_key


def test_enum_values_match_the_design() -> None:
    assert {m.value for m in Kind} == {"llm", "tool"}
    assert {m.value for m in State} == {"open", "closed"}
    assert {m.value for m in Status} == {"success", "failure"}
    assert {m.value for m in LinkType} == {"retry_of"}


@pytest.mark.parametrize("value", ["router", "custom", "LLM", ""])
def test_kind_is_closed(value: str) -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(Kind).validate_python(value)


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


def test_unknown_fields_are_ignored_and_assignment_is_validated() -> None:
    class Sample(PrimitiveModel):
        span_id: SpanId

    sample = Sample.model_validate({"span_id": "a" * 16, "added_in_a_later_minor": 1})
    assert sample.model_dump() == {"span_id": "a" * 16}
    with pytest.raises(ValidationError):
        sample.span_id = "nope"


def test_metadata_keys_are_lowercase_dot_separated() -> None:
    adapter = TypeAdapter(Metadata)
    assert adapter.validate_python({"client.library": "openai", "a": {"x": [1, None]}})
    assert adapter.validate_python({"chronicle.sdk_version": "1"})  # accepted: Chronicle writes it
    for bad in ["Client.library", "client..library", ".client", "client.", "1abc", "a-b", ""]:
        with pytest.raises(ValidationError):
            adapter.validate_python({bad: 1})


def test_trace_labels_must_be_strings() -> None:
    adapter = TypeAdapter(TraceMetadata)
    assert adapter.validate_python({"session_id": "s1"}) == {"session_id": "s1"}
    with pytest.raises(ValidationError):
        adapter.validate_python({"session_id": 1})


def test_reserved_prefix() -> None:
    assert is_reserved_key("chronicle.sdk_version")
    assert not is_reserved_key("chroniclex.a")
    assert not is_reserved_key("client.library")
