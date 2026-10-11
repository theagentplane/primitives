"""Tests for the llm kind: input, output, usage, content blocks and the Envelope wiring."""

import copy
from typing import Any

import pytest
from pydantic import TypeAdapter, ValidationError

from agentplane_primitives.enums import FinishReason, Kind, ModelSource
from agentplane_primitives.models import (
    ContentBlock,
    Envelope,
    LlmInput,
    LlmOutput,
    TextBlock,
    ToolCallBlock,
    ToolInput,
    ToolOutput,
    Usage,
)

CLOSED = {
    "state": "closed",
    "status": "success",
    "started_at": "2026-10-02T10:00:02Z",
    "ended_at": "2026-10-02T10:00:04Z",
}

LLM_ENVELOPE: dict[str, Any] = {
    "envelope_id": "b7ad6b7169203331",
    "span_id": "a1b2c3d4e5f60718",
    "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
    "name": "agent.chat",
    "kind": "llm",
    "attempt": 2,
    "links": [{"type": "retry_of", "envelope_id": "00f067aa0ba902b7"}],
    "envelope_status": CLOSED,
    "input": {
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "What is the weather in Pune?"}],
        "system": "You are a travel assistant.",
        "tools": [{"name": "get_weather", "parameters": {"city": "string"}}],
        "tool_choice": "auto",
        "params": {"temperature": 0.2, "max_tokens": 256, "stop": ["END"]},
        "raw": {"model": "gpt-4o", "messages": [{"role": "user", "content": "..."}]},
    },
    "output": {
        "content": [
            {"type": "text", "text": "Let me check."},
            {
                "type": "tool_call",
                "id": "call_1",
                "name": "get_weather",
                "arguments": {"city": "Pune"},
            },
        ],
        "finish_reason": "tool_calls",
        "provider": "openai",
        "model": "gpt-4o-2024-08-06",
        "model_source": "served",
        "usage": {"input": 812, "cached_read": 0, "cache_write": 0, "output": 96, "reasoning": 0},
        "response_id": "chatcmpl-9x",
        "raw": {"id": "chatcmpl-9x"},
    },
}


def make(**changes: Any) -> dict[str, Any]:
    return {**copy.deepcopy(LLM_ENVELOPE), **changes}


def test_an_llm_envelope_round_trips() -> None:
    envelope = Envelope.model_validate(LLM_ENVELOPE)
    assert envelope.kind is Kind.LLM
    assert isinstance(envelope.input, LlmInput)
    assert isinstance(envelope.output, LlmOutput)
    assert envelope.input.model == "gpt-4o"  # what was asked for
    assert envelope.output.model == "gpt-4o-2024-08-06"  # what served it
    assert envelope.output.model_source is ModelSource.SERVED
    assert envelope.output.finish_reason is FinishReason.TOOL_CALLS
    assert envelope.output.usage == Usage(input=812, output=96)
    assert isinstance(envelope.output.content[1], ToolCallBlock)
    assert Envelope.model_validate_json(envelope.model_dump_json()) == envelope


def test_a_failed_llm_call_has_only_an_error() -> None:
    failed = make(
        output={"error": {"type": "RateLimitError", "message": "429 Too Many Requests"}},
        envelope_status={**CLOSED, "status": "failure"},
    )
    output = Envelope.model_validate(failed).output
    assert isinstance(output, LlmOutput)
    assert output.error is not None
    assert output.provider == "unknown"
    assert output.usage is None
    assert output.model is None


def test_unreported_usage_buckets_are_zero() -> None:
    assert Usage.model_validate({"input": 5}) == Usage(
        input=5, cached_read=0, cache_write=0, output=0, reasoning=0
    )


def test_tool_and_llm_payloads_follow_kind_not_shape() -> None:
    tool = make(kind="tool", input={"raw": {"city": "Pune"}}, output={"raw": 31})
    envelope = Envelope.model_validate(tool)
    assert isinstance(envelope.input, ToolInput)
    assert isinstance(envelope.output, ToolOutput)


def test_content_blocks_are_a_closed_set() -> None:
    adapter: TypeAdapter[Any] = TypeAdapter(ContentBlock)
    assert isinstance(adapter.validate_python({"type": "text", "text": "hi"}), TextBlock)
    for block in ({"type": "image", "url": "x"}, {"text": "no type"}):
        with pytest.raises(ValidationError):
            adapter.validate_python(block)


@pytest.mark.parametrize(
    "changes",
    [
        {"input": {"raw": {"query": "tool-shaped input"}}},  # not an llm input
        {"output": {"raw": {"temperature_c": 31}, "model": "m"}},  # model without model_source
        {"output": {"finish_reason": "eos"}},
        {"output": {"model": "m", "model_source": "guessed"}},
        {"output": {"usage": {"input": -1}}},
        {"output": {"content": [{"type": "text"}]}},
        {"input": {"model": "", "messages": [], "raw": {}}},
        {"input": {"model": "m", "messages": [{"role": "robot", "content": "x"}], "raw": {}}},
        {"input": {"model": "m", "messages": []}},  # raw is always stored
    ],
)
def test_invalid_llm_envelopes_are_rejected(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        Envelope.model_validate(make(**changes))


def test_kind_must_match_the_payload_instances() -> None:
    llm = Envelope.model_validate(LLM_ENVELOPE)
    with pytest.raises(ValidationError):
        Envelope(
            **{**llm.model_dump(), "kind": Kind.TOOL, "input": llm.input, "output": llm.output}
        )


def test_output_must_match_kind_too() -> None:
    llm = Envelope.model_validate(LLM_ENVELOPE)
    with pytest.raises(ValidationError):
        Envelope(
            **{
                **llm.model_dump(),
                "kind": Kind.LLM,
                "input": llm.input,
                "output": ToolOutput(raw=1),
            }
        )


def test_an_existing_envelope_is_accepted_as_is() -> None:
    envelope = Envelope.model_validate(LLM_ENVELOPE)
    assert Envelope.model_validate(envelope) == envelope


def test_a_non_object_payload_is_rejected() -> None:
    with pytest.raises(ValidationError):
        Envelope.model_validate(["not", "an", "object"])
