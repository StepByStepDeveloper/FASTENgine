## What changed

<!-- One paragraph: what and why. -->

## Specification

<!-- For feature work; drop the section for fixes and refactors. -->

- Spec: `docs/specs/NNN-<slug>/spec.adoc` (or: no specification — a fix or refactor)
- Tasks covered: T-NNN-xx
- ADRs: ADR-NNNN (or: none needed)

## Checklist

- [ ] `doit verify` passes (context tree: snippets, links, anchors, layout; the specifications validate)
- [ ] `doit docs_check` passes and `doit docs` builds (documentation tree and site)
- [ ] `doit build` / `doit test` pass (or: no Bazel targets touched)
- [ ] Red step shown: the failing test output is quoted here or attached (feature work)
- [ ] Every criterion covered: `doit trace` reports no uncovered acceptance criteria
- [ ] Existing tests not modified, or the modification is approved by the owner
- [ ] Specification status and content updated in this change if behaviour changed
- [ ] Documentation updated in this change where it applies: an arc42 section, an ADR (`python3 tools/new_adr.py "..."`), a Doxygen block
- [ ] No generated artifact committed (`build/**`, `docs/arc42/images/*.svg`)
