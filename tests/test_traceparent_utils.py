"""Tests for reading and writing the traceparent header."""

import pytest

from agentplane_primitives.models import TraceContext
from agentplane_primitives.utils import (
    format_traceparent,
    from_event,
    new_envelope_id,
    new_trace_id,
    parse_traceparent,
    to_event,
)

TRACE = "4bf92f3577b34da6a3ce929d0e0e4736"
ENVELOPE = "00f067aa0ba902b7"
HEADER = f"00-{TRACE}-{ENVELOPE}-01"


def test_parse_a_valid_header() -> None:
    context = parse_traceparent(HEADER)
    assert context == TraceContext(trace_id=TRACE, parent_envelope_id=ENVELOPE, flags="01")


def test_format_and_parse_round_trip() -> None:
    context = TraceContext(
        trace_id=new_trace_id(), parent_envelope_id=new_envelope_id(), flags="00"
    )
    header = format_traceparent(context)
    assert len(header) == 55
    assert parse_traceparent(header) == context


def test_the_design_example_formats_as_written() -> None:
    context = TraceContext(trace_id=TRACE, parent_envelope_id=ENVELOPE)
    assert format_traceparent(context) == HEADER  # flags default to 01 (sampled)


@pytest.mark.parametrize(
    "bad",
    [
        None,
        "",
        "garbage",
        b"00-" + TRACE.encode() + b"-" + ENVELOPE.encode() + b"-01",
        12345,
        f"01-{TRACE}-{ENVELOPE}-01",  # not version 00
        f"ff-{TRACE}-{ENVELOPE}-01",
        f"00-{TRACE.upper()}-{ENVELOPE}-01",  # W3C requires lowercase
        f"00-{TRACE}-{ENVELOPE.upper()}-01",
        f"00-{TRACE[:-1]}-{ENVELOPE}-01",  # trace id too short
        f"00-{TRACE}0-{ENVELOPE}-01",  # trace id too long
        f"00-{TRACE}-{ENVELOPE[:-1]}-01",
        f"00-{TRACE}-{ENVELOPE}-1",  # flags too short
        f"00-{TRACE}-{ENVELOPE}-zz",
        f"00-{TRACE}-{ENVELOPE}-01-extra",
        f"00-{TRACE}-{ENVELOPE}",  # missing flags
        f" {HEADER}",  # whitespace
        f"{HEADER}\n",
        f"00_{TRACE}_{ENVELOPE}_01",
        f"00-{'0' * 32}-{ENVELOPE}-01",  # all-zero trace id
        f"00-{TRACE}-{'0' * 16}-01",  # all-zero parent id
        "00-" + "é" * 32 + f"-{ENVELOPE}-01",
        pytest.param("0" * 100_000, id="very-long-value"),
    ],
)
def test_malformed_values_give_none_and_never_raise(bad: object) -> None:
    assert parse_traceparent(bad) is None


def test_event_carriers_are_reserved_but_not_implemented() -> None:
    context = TraceContext(trace_id=TRACE, parent_envelope_id=ENVELOPE)
    with pytest.raises(NotImplementedError):
        to_event(context)
    with pytest.raises(NotImplementedError):
        from_event({})
