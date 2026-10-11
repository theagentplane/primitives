# 0004. Keep identity fields at the top level of the envelope and nest status, input, output and metadata

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2026-10-08 |
| Deciders | Susheem Koul, Tisha Chawla |

## Context

The Chronicle technical design (sections 2.2 and 2.3, decision 1) defines the envelope as one
record per boundary crossing with five sections: identity, `envelope_status`, `input`, `output`
and `metadata`. Input and output vary by `kind` (ADR 0002).

In Chronicle 0.5.0 the envelope is flat: `attributes` holds the model, sampling settings and trace
labels under OpenTelemetry keys, status and timing are separate fields, and `Message`,
`ToolCall`, `Usage` and `LLMOutput` are sub-models of input and output.

The design's example payloads (section 2.5) put the identity fields at the top level of the
record, while its section list names `identity` as a section.

## Options considered

### Option A: keep the flat envelope of 0.5.0

- Good: unchanged from 0.5.0.
- Bad: the model and provider overlap between input and metadata that the design removes
  (section 2.3).

### Option B: sections, with a placement rule

The identity fields at the top level, then nested `envelope_status`, `input`, `output` and
`metadata`. Input holds what the caller passed, output holds what is known only from the response (including `usage` and `error`),
metadata holds constant setup in code.

- Good: extension stays inside sections; the model and provider duplication goes away; `usage`
  is part of output because the provider returns it (decision 1).
- Bad: the envelope shape changes from 0.5.0 (flat to sections, `attributes` to `metadata`),
  which is part of the clean break (design sections 12.3 and decision 14).

## Decision

We will use Option B. The identity fields (`envelope_id`, `span_id`, `trace_id`,
`parent_envelope_id`, `name`, `kind`, `attempt`, `links`) sit at the top level of the record, as
in the design's example payloads; `envelope_status`, `input`, `output` and `metadata` are nested
objects. Adding a sibling section later is an optional, additive change (a minor schema bump);
anything narrower is a new payload variant or a new metadata namespace.

## Consequences

- **Good:** one place for each kind of information; the placement rule in section 2.3 decides
  where a new field goes.
- **Bad or risky:** `identity` is a grouping in the documentation, not an object in the payload,
  so a reader must know which top-level fields belong to it. Consumers of 0.5.0 data must
  migrate.
- **Follow-ups:** the `llm` input and output (next PRs), then Trace and Span.

## Impact on other repositories

- **chronicle:** builds and sends this shape (design section 12.3).
- **control-plane:** stores and serves this shape and keeps its own storage layout.
- **tokenops:** reads cost data from `output` only.

## Links

- Design: `docs/rfcs/chronicle-technical-design.md` in chronicle, sections 2.2 to 2.5, decisions
  1 and 14.
- [ADR 0002](0002-closed-kind-enum.md)
