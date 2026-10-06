"""Tests for the closed enums."""

import pytest
from pydantic import TypeAdapter, ValidationError

from agentplane_primitives.enums import Kind, LinkType, State, Status


def test_enum_values_match_the_design() -> None:
    assert {m.value for m in Kind} == {"llm", "tool"}
    assert {m.value for m in State} == {"open", "closed"}
    assert {m.value for m in Status} == {"success", "failure"}
    assert {m.value for m in LinkType} == {"retry_of"}


@pytest.mark.parametrize("value", ["router", "custom", "LLM", ""])
def test_kind_is_closed(value: str) -> None:
    with pytest.raises(ValidationError):
        TypeAdapter(Kind).validate_python(value)
