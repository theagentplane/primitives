# Agent instructions

Shared, versioned domain models (Trace, Span, Envelope) and API models used by Chronicle, the control plane and TokenOps. This package contains data and validation only: no I/O and no business logic.

This file is read by AI coding agents (Claude Code, Codex, Cursor, Copilot and others). Humans
may find it useful too.

## Architecture decisions

Decisions that shape this repository are recorded as ADRs in [`docs/adr/`](docs/adr/README.md).

- **Before changing architecture,** read the ADRs: structure, public interfaces, data formats,
  dependencies or anything shared with another repository. Do not undo an accepted decision
  silently. If a change conflicts with one, say so and propose a new ADR that supersedes it.
- **When asked to record a decision,** or when you make one that meets the criteria in
  `docs/adr/README.md`, write an ADR: copy `docs/adr/template.md`, use the next free number,
  keep it to about a page, and add it to the index.
- **Do not invent reasoning.** If you do not know why something was decided or which alternatives
  were weighed, ask. Leave the status as *Proposed*: the people named as deciders accept it.
- **Never rewrite an accepted ADR.** Supersede it with a new one.

## Change size

- **Estimate before writing code:** lines added plus removed, not counting generated files,
  lockfiles or pure moves and renames.
- **If the estimate is above 400 lines, stop and plan.** Propose to the user a short plan that
  splits the work into logical components (each reviewable on its own, passing CI, in order), and
  wait for agreement before implementing. Open one pull request per component.
- **Keep one change as one thing.** Do not mix unrelated changes into a pull request.
- Staying above 400 lines is acceptable for boilerplate, mechanical changes or generated code,
  but say why in the pull request description.

## Related repositories

[chronicle](https://github.com/theagentplane/chronicle) (edge SDK: record, save, replay) ·
[primitives](https://github.com/theagentplane/primitives) (shared schemas) ·
[control-plane](https://github.com/theagentplane/control-plane) (storage, query, UI) ·
[tokenops](https://github.com/theagentplane/tokenops) (cost governance)
