"""Regenerate the committed JSON Schema files from the public models.

Run from the repository root after changing a model, then commit the result:

    python scripts/generate_schemas.py

Files for models that no longer exist are removed. ``tests/test_schemas.py`` fails in CI when the
committed files differ from what the models generate.
"""

from pathlib import Path

from agentplane_primitives.models.registry import PUBLIC_MODELS
from agentplane_primitives.utils import schema_files

SCHEMAS_DIR = Path(__file__).resolve().parent.parent / "src" / "agentplane_primitives" / "schemas"


def main() -> None:
    files = schema_files(PUBLIC_MODELS)
    for stale in SCHEMAS_DIR.glob("*.json"):
        if stale.name not in files:
            stale.unlink()
            print(f"removed {stale.name}")
    for name, text in files.items():
        (SCHEMAS_DIR / name).write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {name}")
    print(f"{len(files)} schema file(s) up to date")


if __name__ == "__main__":
    main()
