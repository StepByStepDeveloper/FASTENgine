## What changed

<!-- One paragraph: what and why. -->

## Checklist

- [ ] `doit verify` passes (context tree: snippets, links, anchors, layout)
- [ ] `doit docs_check` passes and `doit docs` builds (documentation tree and site)
- [ ] `doit build` / `doit test` pass (or: no Bazel targets touched)
- [ ] Documentation updated in this change where it applies: an arc42 section, an ADR (`python3 tools/new_adr.py "..."`), a Doxygen block
- [ ] No generated artifact committed (`build/**`, `docs/arc42/images/*.svg`)
