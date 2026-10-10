# schemas

**Do not edit the files in this folder by hand.** They are generated from the code.

## What these files are

The rules for our data (a Trace, a Span, an Envelope) are written once, in the code. A schema
is the same rules written as a plain description file: which fields exist, which are required,
what type each one is. Think of it as a form template.

## Why we keep them

- **Other languages can use them.** Anything that is not written in this project's language
  (for example the control plane's web page) can read these files directly.
- **Changes are visible.** When someone changes a rule, these files change too, so a reviewer
  sees in the pull request exactly what every other project will be affected by.
- **Mistakes are caught.** CI checks that these files match the code. If they do not, the
  build fails.

## What to do when you change a model

1. Change the code.
2. If you added a model, add it to `PUBLIC_MODELS` in `src/agentplane_primitives/models/registry.py`.
3. Regenerate the files, from the repository root:

   ```bash
   python scripts/generate_schemas.py
   ```

   It writes one `<ModelName>.json` per public model and removes files for models that no
   longer exist.
4. Commit the code change and the regenerated files together.

If CI says the schemas are out of date, you changed a rule but did not regenerate. Run step 2
and commit again.

The check is `tests/test_schemas.py`, which runs with the rest of the tests
(`pytest`). This folder stays empty until the first Trace, Span or Envelope model is added to
`PUBLIC_MODELS`.
