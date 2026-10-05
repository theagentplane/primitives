# Design

The design for this package is part of the Chronicle technical design:
[chronicle-technical-design.md](https://github.com/theagentplane/chronicle/blob/chronicle1.0/docs/rfcs/chronicle-technical-design.md).

Sections of that document that define what this package contains:

| Section | Defines |
|---|---|
| 2.1 to 2.3 | The three tiers (Trace, Span, Envelope), the envelope sections, input and output by kind |
| 2.4 to 2.6 | Envelope lifecycle, links and retries, trace metadata |
| 2.8 | Versioning (mirrored in [versioning.md](versioning.md)) |
| 2.9 | Enumerations and well-known metadata keys |
| 3.1, 3.2 | Id formats and the `traceparent` carrier |

**Ownership.** The control plane owns the entity schema; this package is where that schema is
defined and shared. Chronicle and TokenOps import it and never define their own copy.

When the design document and this repository disagree, open an issue: the document is the
reference until the models are released.
