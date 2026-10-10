"""Tests for schema generation and the drift check between the models and the committed files."""

from importlib import resources

import pytest
from pydantic import BaseModel

from agentplane_primitives.models.registry import PUBLIC_MODELS
from agentplane_primitives.types import SpanId
from agentplane_primitives.utils import schema_files


class Sample(BaseModel):
    span_id: SpanId
    name: str | None = None


def test_committed_schemas_match_the_models() -> None:
    """Fails when a model changed but the schemas were not regenerated."""
    folder = resources.files("agentplane_primitives").joinpath("schemas")
    committed = {
        entry.name: entry.read_bytes().decode("utf-8")
        for entry in folder.iterdir()
        if entry.name.endswith(".json")
    }
    assert committed == schema_files(PUBLIC_MODELS), (
        "Schemas are out of date. Run: python scripts/generate_schemas.py"
    )


def test_one_file_per_model_with_stable_text() -> None:
    files = schema_files([Sample])
    assert list(files) == ["Sample.json"]
    text = files["Sample.json"]
    assert text.endswith("}\n")
    assert text == schema_files([Sample])["Sample.json"]
    assert text.index('"properties"') < text.index('"title"')  # keys are sorted


def test_schema_carries_the_id_rules() -> None:
    text = schema_files([Sample])["Sample.json"]
    assert "^[0-9a-f]{16}$" in text
    assert "not all zeros" in text


def test_two_models_with_the_same_name_are_rejected() -> None:
    class Other(BaseModel):
        pass

    Other.__name__ = "Sample"
    with pytest.raises(ValueError, match="Sample"):
        schema_files([Sample, Other])
