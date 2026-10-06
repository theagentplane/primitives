"""Tests for the metadata key and label rules."""

import pytest
from pydantic import TypeAdapter, ValidationError

from agentplane_primitives.types.metadata_types import Metadata, TraceMetadata


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
