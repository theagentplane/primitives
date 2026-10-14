# 0007. Trace carries a mutable `attributes` dict beside the write-once labels

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-15 |
| Deciders | Susheem Koul |

## Context

`Trace.metadata` holds string labels that are written once and indexed. The control plane and
TokenOps need trace-level state that changes after the trace starts and is not written by
Chronicle (first case: a halt flag that stops a run). Without a place on the entity, each consumer
keeps a side table keyed by `trace_id` that must be kept in sync with the trace.

## Options considered

### Option A: control-plane-only columns or side tables

- Good: no change here.
- Bad: the stored trace and the entity drift; every consumer invents its own table.

### Option B: `Trace.attributes`, a general-purpose dict of JSON values

- Good: state lives on the entity; no side table; additive and optional.
- Bad: an untyped bag can become a dumping ground.

## Decision

We will add `Trace.attributes: dict[MetadataKey, JsonValue]`, default `{}`. It is mutable, written
by the control plane or a consumer and never by Chronicle. Consumers namespace their keys
(`tokenops.halted`). Labels in `metadata` stay write-once strings.

## Consequences

- **Good:** halt state and similar flags are part of the trace and travel with it.
- **Bad or risky:** keys are not validated beyond the metadata key pattern; a consumer that needs
  a typed contract must document it. Keys in this dict are not indexed.
- **Follow-ups:** the control plane decides merge semantics when it exposes a write route.

## Impact on other repositories

- control-plane: stores and serves it; uses it for the halt flag.
- tokenops: namespaces its keys; reads the halt flag through the control plane.
- chronicle: none; it never writes `attributes`.
