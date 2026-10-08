"""``PUBLIC_MODELS``: the models that get a committed JSON Schema file.

Add a model here in the same pull request that introduces it, then run
``python scripts/generate_schemas.py`` and commit the new file. Helper models that only appear
inside another model do not need an entry: they are included in that model's schema.
"""

from pydantic import BaseModel

PUBLIC_MODELS: tuple[type[BaseModel], ...] = ()
