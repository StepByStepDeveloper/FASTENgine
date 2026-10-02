# SCRATCHPAD — active task

Operational memory of **one** task: the agent writes and rereads it while working, and clears it when the task ends. This is a working note, not a report — keep it short.

**Status**: complete — the SDD + ADR + TDD batch landed as `a58b75f`; the follow-up consistency pass answering the external review is applied, gate-green and committed on the owner's go. Both pushed to origin/main.

## Objective

Adopt the process artifacts of the SDD + ADR + TDD method (the specifications, process conventions, gates, skills/commands, an ADR recording the decision) and restructure the development manual into a sequential walkthrough with progressive disclosure and a glossary.

## Status

- [x] tools/spec_check.py + tools/trace.py; `doit spec_check` inside `verify`, new `doit trace`
- [x] docs/specs/: README + `_templates/` (spec / plan / tasks)
- [x] conventions: `process.md` (new), `testing.md` (+TDD), `docs.md` (+specs), `style/documentation.md` (+`@covers`/`@implements`)
- [x] manual: README reading path, `process.md`, `getting-started.md`, `glossary.md`, `documentation/specs.md`
- [x] .agents: skills `write-spec` / `tdd-cycle`; commands `new-spec` / `implement-task`; persona `test-reviewer`; eval `spec-first-discipline`; guardrails + hook `spec-gate-on-edit`
- [x] ADR-0005 (through the generator) + Doxyfile aliases (verified with doxygen)
- [x] AGENTS.md (<4000 chars), pre-commit, CI, PR template, root README, hooks, verify-rules skill
- [x] gates: `doit verify` / `spec_check` / `docs_check` / `trace` — green; `docs` / `build` / `test` re-run before hand-off
- [x] consistency pass after the external review: terminology ("context tree" vs "the specifications"), stage order (Specify -> Decide -> Approve), walkthrough AC numbering, EARS example, advisory-vs-blocking phrasing, entry-point wording — `doit verify` / `docs_check` / `trace` green again; committed on the owner's go

## Discovered Issues

- `AGENTS.md` is gate-protected (an edit raises the approval prompt): the pending review line was applied on the owner's go — "carries its documentation and context, not engine code". Size 3965/4000 chars (~35 left).
- `verify_rule_docs.py` (a copy of the agent-side skill `agent-rules-docs`) keeps "specification trees" in its docstring — left as-is to stay in sync with the upstream skill; change the skill first if the term must go.
- `plan-feature` was folded into `write-spec` (one skill for spec -> plan -> tasks) instead of a separate skill.
- The pilot feature (spec 001) remains a separate, human-involving step — not part of this change.

## Next action

Run the pilot feature (spec 001) — the first run of the loop through `docs/specs/`.
