"""Turn the public models into JSON Schema text (design section 2.8).

This is pure: it returns file names and file contents and touches no disk. Writing the files is
the job of ``scripts/generate_schemas.py``; checking that the committed files are current is
``tests/test_schemas.py``. The output is stable (sorted keys, fixed indentation, final newline),
so an unchanged model always produces byte-identical text.
"""

import json
from collections.abc import Iterable

from pydantic import BaseModel


def schema_files(models: Iterable[type[BaseModel]]) -> dict[str, str]:
    """Return ``{file name: schema text}``, one ``<ModelName>.json`` entry per model."""
    files: dict[str, str] = {}
    for model in models:
        name = f"{model.__name__}.json"
        if name in files:
            raise ValueError(f"two public models are called {model.__name__}")
        files[name] = json.dumps(model.model_json_schema(), indent=2, sort_keys=True) + "\n"
    return files
