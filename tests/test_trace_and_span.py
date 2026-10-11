"""Tests for the Trace and Span entities."""

from typing import Any

import pytest
from pydantic import ValidationError

from agentplane_primitives.enums import State, Status
from agentplane_primitives.models import Span, Trace

TRACE_ID = "4bf92f3577b34da6a3ce929d0e0e4736"
START = "2026-10-02T10:00:00Z"
END = "2026-10-02T10:00:05Z"


def test_a_trace_with_labels() -> None:
    trace = Trace.model_validate(
        {
            "trace_id": TRACE_ID,
            "name": "chat turn",
            "metadata": {"session_id": "s-1", "message_id": "m-7", "user_id": "u-3"},
            "state": "open",
        }
    )
    assert trace.state is State.OPEN
    assert trace.metadata["session_id"] == "s-1"
    assert trace.schema_version == "0.1"
    assert trace.started_at is None  # derived by the control plane
    assert Trace.model_validate_json(trace.model_dump_json()) == trace


def test_a_trace_has_no_status() -> None:
    trace = Trace.model_validate({"trace_id": TRACE_ID, "state": "closed", "status": "success"})
    assert not hasattr(trace, "status")
    assert "status" not in trace.model_dump()


@pytest.mark.parametrize(
    "changes",
    [
        {"trace_id": "0" * 32},
        {"state": "paused"},
        {"name": ""},
        {"metadata": {"session_id": 7}},  # labels are strings
        {"metadata": {"Session Id": "x"}},
        {"started_at": "2026-10-02T10:00:00"},  # no time zone
    ],
)
def test_invalid_traces_are_rejected(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        Trace.model_validate({"trace_id": TRACE_ID, "state": "open", **changes})


FIRST_SPAN: dict[str, Any] = {
    "span_id": "a1b2c3d4e5f60718",
    "trace_id": TRACE_ID,
    "service": "agent-a",
    "state": "open",
    "started_at": START,
}


def test_the_first_span_has_no_parent_and_a_downstream_span_names_one() -> None:
    first = Span.model_validate(FIRST_SPAN)
    assert first.parent_envelope_id is None
    downstream = Span.model_validate(
        {**FIRST_SPAN, "span_id": "b2c3d4e5f6071829", "parent_envelope_id": "00f067aa0ba902b7"}
    )
    assert downstream.parent_envelope_id == "00f067aa0ba902b7"


def test_a_span_closes_with_a_status() -> None:
    closed = Span.model_validate(
        {**FIRST_SPAN, "state": "closed", "status": "failure", "ended_at": END}
    )
    assert closed.status is Status.FAILURE
    assert closed.metadata == {}
    assert Span.model_validate_json(closed.model_dump_json()) == closed


@pytest.mark.parametrize(
    "changes",
    [
        {"status": "success"},  # open span with a result
        {"ended_at": END},  # open span with an end time
        {"state": "closed"},  # closed with neither
        {"state": "closed", "status": "success"},  # closed without ended_at
        {"state": "closed", "status": "success", "ended_at": "2026-10-02T09:00:00Z"},
        {"service": ""},
        {"span_id": "0" * 16},
        {"parent_envelope_id": "xyz"},
        {"status": "aborted", "state": "closed", "ended_at": END},
    ],
)
def test_invalid_spans_are_rejected(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        Span.model_validate({**FIRST_SPAN, **changes})
