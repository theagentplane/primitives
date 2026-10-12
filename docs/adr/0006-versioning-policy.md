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

> **Drafted by Claude at the maintainers' request.** The design records the rules, not the
> alternatives that were weighed, so the options below are candidates written for this ADR, not a
> record of what was discussed. The deciders must confirm, correct or replace them before
> accepting.

### Option A: one version only, the package SemVer

- Good: nothing extra to carry on payloads.
- Bad: a stored payload does not say which schema wrote it, which matters because the control
  plane reads two majors and upconverts on read.

### Option B: allow breaking changes in minor releases before 1.0

The usual allowance for 0.x versions.

- Good: easier to change shape while the models are young.
- Bad: each of the three consumers can break on a minor upgrade, which is why the rules here ask
  them to pin the exact minor before 1.0 and treat changes as additive.

### Option C: two versions, additive within a major (the policy as written)

- Good: a payload names its schema version; consumers know what an upgrade may change.
- Bad: new enum members force consumers to upgrade before emitters; the control plane carries
  upconversion for the previous major.

## Decision

We will take Option C: two versions and an additive-only rule:

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
