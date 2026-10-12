# 0006. Version the package and the schema separately, additive within a major

| Field | Value |
|---|---|
| Status | Proposed |
| Date | 2026-10-12 |
| Deciders | Susheem Koul, Tisha Chawla |

## Context

Three repositories depend on this package: Chronicle (writes envelopes), the control plane
(stores and serves them) and TokenOps (reads cost data). Compatibility between them is a contract.
The policy is stated in the Chronicle technical design (section 2.8, decisions 9 and 15) and
written out in [docs/versioning.md](../versioning.md); this ADR records it as a decision.

## Options considered

The design records the rules, not the alternatives that were weighed. The deciders should add
those here before accepting this ADR; none is invented in this draft.

## Decision

We will use two versions and an additive-only rule:

- **Package version** follows SemVer. **`schema_version`** (`major.minor`) is carried on every
  persisted payload, and the package major equals the schema major.
- **Additive-only within a major.** New optional fields are allowed and readers ignore unknown
  fields. A new member of a closed enum, including a new `kind`, is additive for the writer, but a
  reader on an older minor rejects the unknown value, so consumers upgrade before emitters.
- **A breaking change is a new major.** The control plane accepts the current and the previous
  major and upconverts on read. Release order for a breaking change: primitives, then the control
  plane, then Chronicle and TokenOps.
- **Pre-1.0**, consumers pin the exact minor; from 1.0, `>=1.2,<2`.
- **Safety nets:** consumers import these models rather than write their own parsers, and the
  committed JSON Schema is checked against the models in CI.

## Consequences

- **Good:** each consumer can tell what an upgrade may change; one definition of every payload.
- **Bad or risky:** consumers must upgrade before emitters whenever an enum gains a member; the
  control plane has to carry upconversion for the previous major; before 1.0 every consumer must
  bump a pin for each minor.
- **Follow-ups:** a shared golden corpus of example payloads for consumers that parse by hand is
  future scope (design section 12.1).

## Impact on other repositories

- **chronicle, control-plane, tokenops:** pin the exact minor of `agentplane-primitives` until
  1.0 and follow the release order above for breaking changes.

## Links

- Design: `docs/rfcs/chronicle-technical-design.md` in chronicle, section 2.8 and decisions 9
  and 15.
- [Versioning policy](../versioning.md)
- [CHANGELOG](../../CHANGELOG.md)
