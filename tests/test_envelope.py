"""Tests for the Envelope and the tool input, output, error and link models."""

import copy
from typing import Any

import pytest
from pydantic import ValidationError

from agentplane_primitives.enums import Kind, LinkType, Status
from agentplane_primitives.models import ABORT_CALL, Envelope

FIRST: dict[str, Any] = {
    "envelope_id": "00f067aa0ba902b7",
    "span_id": "a1b2c3d4e5f60718",
    "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
    "parent_envelope_id": None,
    "name": "search.web",
    "kind": "tool",
    "attempt": 1,
    "envelope_status": {
        "state": "closed",
        "status": "failure",
        "started_at": "2026-10-02T10:00:00Z",
        "ended_at": "2026-10-02T10:00:01Z",
    },
    "input": {"raw": {"query": "weather in Pune"}},
    "output": {"error": {"type": "RateLimitError", "message": "429 Too Many Requests"}},
}

RETRY: dict[str, Any] = {
    **FIRST,
    "envelope_id": "b7ad6b7169203331",
    "attempt": 2,
    "links": [{"type": "retry_of", "envelope_id": "00f067aa0ba902b7"}],
    "envelope_status": {
        "state": "closed",
        "status": "success",
        "started_at": "2026-10-02T10:00:02Z",
        "ended_at": "2026-10-02T10:00:04Z",
    },
    "output": {"raw": {"temperature_c": 31}},
}


def make(**changes: Any) -> dict[str, Any]:
    return {**copy.deepcopy(FIRST), **changes}


def test_a_failed_call_and_its_retry_round_trip() -> None:
    first = Envelope.model_validate(FIRST)
    retry = Envelope.model_validate(RETRY)
    assert first.schema_version == "0.1"
    assert first.kind is Kind.TOOL
    assert first.envelope_status.status is Status.FAILURE
    assert first.output is not None
    assert first.output.error is not None
    assert first.output.error.type == "RateLimitError"
    assert retry.attempt == 2
    assert retry.links[0].type is LinkType.RETRY_OF
    assert retry.links[0].envelope_id == first.envelope_id
    assert Envelope.model_validate_json(retry.model_dump_json()) == retry


def test_defaults_and_unknown_fields() -> None:
    minimal = make(attempt=None)
    del minimal["attempt"]
    envelope = Envelope.model_validate({**minimal, "added_later": True})
    assert envelope.attempt == 1
    assert envelope.links == []
    assert envelope.metadata == {}
    assert not hasattr(envelope, "added_later")


def test_open_envelope_needs_no_output() -> None:
    open_envelope = make(
        envelope_status={"state": "open", "started_at": "2026-10-02T10:00:00Z"}, output=None
    )
    assert Envelope.model_validate(open_envelope).output is None


def test_abort_is_a_failure_with_a_reserved_error_type() -> None:
    aborted = make(output={"error": {"type": ABORT_CALL, "message": "budget exceeded"}})
    envelope = Envelope.model_validate(aborted)
    assert envelope.output is not None
    assert envelope.output.error is not None
    assert envelope.output.error.type == "AbortCall"


@pytest.mark.parametrize(
    "changes",
    [
        {"kind": "router"},
        {"kind": "llm"},  # no llm input and output models yet
        {"output": None},  # closed without an output
        {"attempt": 0},
        {"name": ""},
        {"trace_id": "0" * 32},
        {"span_id": "A" * 16},
        {"input": {"raw": ["not", "an", "object"]}},
        {"input": {}},
        {"links": [{"type": "joined", "envelope_id": "00f067aa0ba902b7"}]},
        {"output": {"error": {"type": "", "message": "x"}}},
        {"metadata": {"Bad Key": 1}},
        {"schema_version": "v1"},
    ],
)
def test_invalid_envelopes_are_rejected(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        Envelope.model_validate(make(**changes))
