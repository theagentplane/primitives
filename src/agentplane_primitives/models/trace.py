"""``Trace``: one request across many services (design sections 2.1, 2.2 and 2.6).

A Trace has no result of its own (OpenTelemetry does not either): ``state`` is ``open`` while any
of its spans is open and ``closed`` after, and "did it succeed" is a view the control plane can
compute. ``started_at`` and ``ended_at`` are derived by the control plane, so both are optional
here.

``metadata`` holds the trace-level labels, written once and not copied onto every envelope. The
labels are strings, because they are indexed and filtered on. Well-known keys: ``session_id``,
``message_id`` and ``user_id``. "Written once" is enforced by the control plane, not by this model.

``attributes`` is the general-purpose counterpart: any JSON value, **mutable**, and written by the
control plane or a consumer such as TokenOps, never by Chronicle. It carries trace-level state that
is not a label, for example a halt flag. Keys follow the metadata conventions; consumers namespace
their keys (``tokenops.halted``). The control plane replaces the whole dict or merges keys.
"""

from pydantic import AwareDatetime, Field

from agentplane_primitives.enums import State
from agentplane_primitives.models.base import PrimitiveModel
from agentplane_primitives.types import (
    SCHEMA_VERSION,
    Metadata,
    SchemaVersion,
    TraceId,
    TraceMetadata,
)


class Trace(PrimitiveModel):
    """One request, from the first service that handled it to the last."""

    schema_version: SchemaVersion = SCHEMA_VERSION
    trace_id: TraceId
    name: str | None = Field(default=None, min_length=1, description="Optional human label.")
    metadata: TraceMetadata = Field(default_factory=dict, description="Trace labels.")
    attributes: Metadata = Field(
        default_factory=dict,
        description="Mutable trace-level state written by the control plane or a consumer.",
    )
    state: State
    started_at: AwareDatetime | None = None
    ended_at: AwareDatetime | None = None
