"""``PrimitiveModel``: the base class every model in this package inherits from.

It holds the settings all models share, so they are decided once (design section 2.8).
"""

from pydantic import BaseModel, ConfigDict


class PrimitiveModel(BaseModel):
    """Shared model settings.

    - Unknown fields are ignored on read. This only matters when writer and reader run
      different versions (for example during a rolling upgrade); the control plane keeps the
      full original payload, so nothing is lost.
    - Assigning a bad value to a field is validated, not silently accepted.
    """

    model_config = ConfigDict(extra="ignore", validate_assignment=True)
