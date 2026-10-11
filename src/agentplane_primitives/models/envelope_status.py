"""``EnvelopeStatus``: the lifecycle and result of an envelope (design sections 2.2 and 2.4).

An envelope is one record that is mutable until it is closed. While ``open`` it has a start time
and nothing else; once ``closed`` it has a result and an end time. To close an envelope, build a
new ``EnvelopeStatus``: changing the fields one by one would pass through an invalid state.
"""

from pydantic import AwareDatetime, model_validator

from agentplane_primitives.enums import State, Status
from agentplane_primitives.models.base import PrimitiveModel
from agentplane_primitives.utils.lifecycle_utils import check_lifecycle


class EnvelopeStatus(PrimitiveModel):
    """State, result and timing of an envelope. Times must carry a time zone."""

    state: State
    status: Status | None = None
    started_at: AwareDatetime
    ended_at: AwareDatetime | None = None

    @model_validator(mode="after")
    def _check_lifecycle(self) -> "EnvelopeStatus":
        check_lifecycle(self.state, self.status, self.started_at, self.ended_at, "envelope")
        return self
