# 0005. Model a request as three tiers: Trace, Span and Envelope

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-12 |
| Deciders | Susheem Koul, Tisha Chawla |

## Context

The Chronicle technical design (section 2.1) describes one request as a Trace across many
services, a Span for one service's handling of it (one process, one agent run), and an Envelope
for one boundary crossing inside the span.

OpenTelemetry has only spans, and uses them both for a request at a service edge and for each
action inside it. In Chronicle 0.5.0, `sequence` and `invocation_index` are per-process counters
that replay assumes are global.

## Options considered

### Option A: two tiers, as OpenTelemetry does

A trace made of spans, where each action inside a service is also a span.

- Good: one fewer entity and one fewer id (the design names this as the cost of the third tier).
- Bad: none of the benefits listed for the split: a natural unit for replay and tests, parallel
  runs that do not interfere, local ordering, and retention and ownership that attach cleanly.

### Option B: three tiers

Trace, then Span, then Envelope, with the Span identified by `trace_id` plus `span_id`.

- Good: replay and tests have a natural unit, a Span. Two concurrent agent runs append to their
  own spans and do not interfere. `sequence` and `invocation_index` become counters inside one
  span, so no distributed ordering problem exists. Retention and ownership attach to a span.
- Bad: one extra entity and one extra id.

## Decision

We will model a request as three tiers: Trace, Span and Envelope. A Span's parent is the Envelope
in the caller's span that made the outbound call (`parent_envelope_id`), which is the only link
between services. A Trace has only a `state`; a Span and an Envelope have a `state` and a
`status`. In OpenTelemetry terms a Chronicle Span maps to a server span and an Envelope to a
child span; that mapping is the control plane's concern.

## Consequences

- **Good:** the benefits listed under Option B.
- **Bad or risky:** an extra entity to create, store and keep consistent. A Trace has no status
  of its own, so "did the request succeed" is a view the control plane has to compute.
- **Follow-ups:** the `traceparent` carrier (next PR) carries the caller's envelope id as the
  link between spans.

## Impact on other repositories

- **chronicle:** records one span per request handled and envelopes inside it; counters are
  per span.
- **control-plane:** stores the three entities, resolves an envelope id to its span, and maps
  them to OpenTelemetry on export.
- **tokenops:** none beyond reading envelopes.

## Links

- Design: `docs/rfcs/chronicle-technical-design.md` in chronicle, sections 2.1 and 2.2.
- [ADR 0002](0002-closed-kind-enum.md), [ADR 0004](0004-envelope-sections.md)
