# 0002. Define envelope `kind` as a closed enum with two members

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-06 |
| Deciders | Susheem Koul, Tisha Chawla |

## Context

Every envelope has a `kind` that selects the shape of its input and output (design sections 2.3
and 2.9). In Chronicle 0.5.0, `kind` is a free string, and `router` and `custom` are in use
alongside `llm` and `tool`. Consumers such as TokenOps read the envelope by kind, and replay
needs to know how to handle each one. A router is either an LLM call or, if it is a plain
function, a tool; delegating work to another agent is an outbound call, which is a tool envelope
(the link between the two services is carried by `traceparent`).

## Options considered

### Option A: keep `kind` a free string

What 0.5.0 does today.

- Good: unchanged from 0.5.0.
- Bad: it allows values such as `router` and `custom`, which the design retires (section 2.3).

### Option B: closed enum defined in this package

`kind` is `llm` or `tool`. Any other value is rejected at validation.

- Good: a value outside the enum is rejected at validation (section 2.3).
- Bad: adding a kind is a schema change made in this package (section 2.8).

## Decision

We will define `kind` as a closed enum in this package with the members `llm` and `tool`, and
reject every other value, including custom and unregistered kinds. `router` and `custom` from
0.5.0 are retired; both become `tool`.

## Consequences

- **Good:** one definition of `kind`, shared by Chronicle, the control plane and TokenOps.
- **Bad or risky:** a new kind is additive for the writer, but a reader on an older minor rejects
  it, so consumers must upgrade before emitters (`docs/versioning.md`). Users cannot invent their
  own kinds.
- **Follow-ups:** the input and output variants selected by `kind` arrive with the envelope
  (tool first, then llm).

## Impact on other repositories

- **chronicle:** declaring a boundary with any other kind fails at declaration time; `router`
  and `custom` become `tool` (design section 12.3).
- **control-plane:** validates ingested envelopes against this enum.
- **tokenops:** `delegate` is removed from its list of observation kinds, leaving `llm | tool`.

## Links

- Design: `docs/rfcs/chronicle-technical-design.md` in chronicle, sections 2.3 and 2.9, decision
  12.
- [Versioning policy](../versioning.md)
