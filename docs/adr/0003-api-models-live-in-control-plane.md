# 0003. Keep HTTP request and response wrappers out of primitives

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-06 |
| Deciders | Susheem Koul, Tisha Chawla |

## Context

The Chronicle technical design (sections 2.8 and 10.1, and the layer table in section 1.1) lists
"the API request and response models" as part of this package, next to Trace, Span and
Envelope. Decision 9 of that design says the control plane owns the schema and that Chronicle
"must not depend on server code".

Trace, Span and Envelope are the records the whole system stores and passes around. They are
data, not requests. The control plane will use them as the body of its requests and responses,
while the endpoints, status codes and the rest of the HTTP layer are its own concern.

## Options considered

### Option A: API models stay in primitives (the design as written)

- Good: one place for everything on the wire; Chronicle and the control plane share the same
  request and result shapes.
- Bad: this package takes on the shape of one service's HTTP API, which changes with that
  service rather than with the data.

### Option B: the control plane owns all API models, and Chronicle depends on primitives through it

- Good: nothing HTTP-specific in primitives.
- Bad: Chronicle, an SDK that runs inside other people's services, would install the control
  plane's dependencies and be tied to its releases. This conflicts with decision 9.

### Option C: primitives holds only the entities; the control plane owns the HTTP wrappers

Requests and responses reuse primitives types as their bodies (an upsert-span body is a `Span`; a
batch of envelopes is a list of `Envelope`). Wrappers that exist only because of the HTTP API
(the write result and the error body) belong to the control plane. Chronicle imports primitives
directly.

- Good: primitives stays about the data; Chronicle keeps one small dependency; entities have a
  single definition.
- Bad: Chronicle must read the write result and error body without a shared model, so it needs a
  few lines of its own code and a contract test against the control plane.

## Decision

We will take Option C. Primitives defines the entities, ids, enums, metadata rules, the
`traceparent` carrier and the committed JSON Schema, and no HTTP request or response wrappers.

## Consequences

- **Good:** a smaller package with a stable surface; the control plane can change its API without
  a primitives release.
- **Bad or risky:** the result and error shapes are defined in one repository and read in
  another, so drift is possible until a contract test exists. If those shapes grow, moving them
  into primitives later is an additive change.
- **Follow-ups:** the planned primitives PR for API models is dropped. The control plane
  defines the wrappers; Chronicle adds a contract test.

## Impact on other repositories

- **chronicle:** the technical design (sections 1.1, 2.8, 10.1) is updated to match. The client
  imports primitives for entities and parses the write result and error body itself.
- **control-plane:** defines the HTTP wrappers and reuses primitives entities as bodies.
- **tokenops:** none.

## Links

- Design: `docs/rfcs/chronicle-technical-design.md` in chronicle, sections 1.1, 2.8, 10.1 and
  decision 9.
