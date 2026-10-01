# SCRATCHPAD — active task

Operational memory of **one** task: the agent writes and rereads it while working, and clears it when the task ends. This is a working note, not a report — keep it short.

**Status**: complete — the SDD + ADR + TDD process artifacts are adopted and the development manual is rebuilt as a sequential walkthrough; awaiting the owner's review of the batch (nothing committed).

## Objective

Adopt the process artifacts of the SDD + ADR + TDD method (spec tree, process conventions, gates, skills/commands, an ADR recording the decision) and restructure the development manual into a sequential walkthrough with progressive disclosure and a glossary.

## Status

- [x] tools/spec_check.py + tools/trace.py; `doit spec_check` inside `verify`, new `doit trace`
- [x] docs/specs/: README + `_templates/` (spec / plan / tasks)
- [x] conventions: `process.md` (new), `testing.md` (+TDD), `docs.md` (+specs), `style/documentation.md` (+`@covers`/`@implements`)
- [x] manual: README reading path, `process.md`, `getting-started.md`, `glossary.md`, `documentation/specs.md`
- [x] .agents: skills `write-spec` / `tdd-cycle`; commands `new-spec` / `implement-task`; persona `test-reviewer`; eval `spec-first-discipline`; guardrails + hook `spec-gate-on-edit`
- [x] ADR-0005 (through the generator) + Doxyfile aliases (verified with doxygen)
- [x] AGENTS.md (<4000 chars), pre-commit, CI, PR template, root README, hooks, verify-rules skill
- [x] gates: `doit verify` / `spec_check` / `docs_check` / `trace` — green; `docs` / `build` / `test` re-run before hand-off

## Discovered Issues

- `AGENTS.md` is gate-protected (measured size < 4000 chars); headroom after this task: ~50 characters.
- `plan-feature` was folded into `write-spec` (one skill for spec -> plan -> tasks) instead of a separate skill.
- The pilot feature (spec 001) remains a separate, human-involving step — not part of this change.

## Next action

Owner review of the batch; then the pilot feature becomes the first run of the loop (spec 001 through `docs/specs/`).
