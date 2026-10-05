"""AgentPlane primitives: shared, versioned domain objects.

Used by Chronicle, the control plane and TokenOps. This package holds data models only:
no I/O and no business logic. The entities (Trace, Span, Envelope) and API models are
added in later releases; see ``docs/design.md``.
"""

from agentplane_primitives._version import __version__

__all__ = ["__version__"]
