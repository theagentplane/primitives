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

- [ ] Change is under about 400 lines, or the description links the split plan or says why it is one change
- [ ] Tests added or updated
- [ ] `src/agentplane_primitives/schemas/` regenerated (if a model changed)
- [ ] CHANGELOG entry added and classified as compatible or breaking
- [ ] `ruff`, `mypy` and `pytest` pass locally
