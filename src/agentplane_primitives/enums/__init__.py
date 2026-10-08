"""Closed sets of values shared by every entity (design section 2.9).

Each enum has its own module. A new member of any enum is a schema change: see
``docs/versioning.md``. Enums that exist only inside one kind of payload (``finish_reason``,
``model_source``, content block types, message roles) live with that payload.
"""

from agentplane_primitives.enums.base_enum import BaseEnum
from agentplane_primitives.enums.kind import Kind
from agentplane_primitives.enums.link_type import LinkType
from agentplane_primitives.enums.state import State
from agentplane_primitives.enums.status import Status

__all__ = ["BaseEnum", "Kind", "LinkType", "State", "Status"]
