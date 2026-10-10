"""Closed sets of values shared by the entities (design section 2.9).

Each enum has its own module. A new member of any enum is a schema change: see
``docs/versioning.md``.
"""

from agentplane_primitives.enums.base_enum import BaseEnum
from agentplane_primitives.enums.finish_reason import FinishReason
from agentplane_primitives.enums.kind import Kind
from agentplane_primitives.enums.link_type import LinkType
from agentplane_primitives.enums.message_role import MessageRole
from agentplane_primitives.enums.model_source import ModelSource
from agentplane_primitives.enums.state import State
from agentplane_primitives.enums.status import Status

__all__ = [
    "BaseEnum",
    "FinishReason",
    "Kind",
    "LinkType",
    "MessageRole",
    "ModelSource",
    "State",
    "Status",
]
