# corpus

Golden example payloads, used as shared test vectors.

- `valid/`: payloads that must validate against the current schema.
- `invalid/`: payloads that must be rejected (for example an unknown envelope `kind`).

Every consumer repository (Chronicle, control plane, TokenOps) validates against this corpus in
its own CI, so a change here that breaks a consumer is caught before release.

Conventions:

- One JSON file per case, named for what it demonstrates (`llm-success.json`,
  `llm-retry-of.json`, `invalid-unknown-kind.json`).
- Provider conformance cases pair a raw provider response with its expected canonical form.
- Never put real production data in the corpus.
