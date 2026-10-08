"""``Link``: a typed pointer from one envelope to another (design section 2.5).

Retries are declared explicitly: an envelope that retries an earlier one carries a ``retry_of``
link to it. The linked envelope is in the same trace.
"""

from agentplane_primitives.enums import LinkType
from agentplane_primitives.models.base import PrimitiveModel
from agentplane_primitives.types import EnvelopeId


class Link(PrimitiveModel):
    """A relationship to another envelope in the same trace."""

    type: LinkType
    envelope_id: EnvelopeId
