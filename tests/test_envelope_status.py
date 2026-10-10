"""Tests for the envelope lifecycle rules."""

import pytest
from pydantic import ValidationError

from agentplane_primitives.enums import State, Status
from agentplane_primitives.models import EnvelopeStatus

START = "2026-10-02T10:00:00Z"
END = "2026-10-02T10:00:01Z"


def test_open_envelope_has_only_a_start_time() -> None:
    status = EnvelopeStatus.model_validate({"state": "open", "started_at": START})
    assert status.state is State.OPEN
    assert status.status is None


def test_closed_envelope_has_a_result_and_an_end_time() -> None:
    status = EnvelopeStatus.model_validate(
        {"state": "closed", "status": "failure", "started_at": START, "ended_at": END}
    )
    assert status.status is Status.FAILURE


@pytest.mark.parametrize(
    "payload",
    [
        {"state": "open", "status": "success", "started_at": START},
        {"state": "open", "started_at": START, "ended_at": END},
        {"state": "closed", "started_at": START, "ended_at": END},
        {"state": "closed", "status": "success", "started_at": START},
        {"state": "closed", "status": "success", "started_at": END, "ended_at": START},
        {"state": "open", "started_at": "2026-10-02T10:00:00"},  # no time zone
        {"state": "paused", "started_at": START},
    ],
)
def test_invalid_lifecycles_are_rejected(payload: dict[str, str]) -> None:
    with pytest.raises(ValidationError):
        EnvelopeStatus.model_validate(payload)
