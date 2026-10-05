# schemas

Generated JSON Schema for every public model, one file per model.

- **Do not edit by hand.** The files are generated from the pydantic models.
- **Committed on purpose.** Non-Python consumers can use them directly, and reviewers see the
  schema effect of every model change in the diff.
- **Drift-checked.** CI regenerates the schemas and fails if they differ from what is committed.

This directory is empty until the models land (see the roadmap in the top-level README).
