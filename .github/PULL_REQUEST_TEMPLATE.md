## Summary

<!-- What changes and why? One thing per pull request. -->

## Related issue

<!-- e.g. Closes #123 -->

## Compatibility

- [ ] Compatible (additive only)
- [ ] Breaking (new major; migration noted below)

<!-- If a model, enum or id format changed: which consumers (Chronicle, control plane, TokenOps)
     are affected and what must each do to migrate? -->

## Checklist

- [ ] Tests added or updated
- [ ] `schemas/` regenerated (if a model changed)
- [ ] Corpus case added in `corpus/valid/` (and `corpus/invalid/` where relevant)
- [ ] CHANGELOG entry added and classified as compatible or breaking
- [ ] `ruff`, `mypy` and `pytest` pass locally
