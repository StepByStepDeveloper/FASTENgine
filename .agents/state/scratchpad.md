# SCRATCHPAD — active task

Operational memory of **one** task: the agent writes and rereads it while working, and clears it when the task ends. This is a working note, not a report — keep it short.

**Status**: done — the restructure is in place and all gates are green (`doit verify`, `doit docs_check`, `doit trace`; earlier full runs incl. `doit docs` were green too); awaiting the owner's review and an explicit commit request. The agents chapter now lives at `docs/development/working-with-agents.md`, renamed out of the harness's write-gated basenames.

## Objective

1. Describe the repository's structure and the purpose of its directories in the development manual — including the agent-context tree (`.agents/`).
2. Describe how to develop with agents — a manual chapter on working with them.
3. Adapt the process: planning (spec + ADRs + plan + tasks) is agreed at architectural review and feature planning; implementation is deferrable and separate in time; the process and its docs work with no AI at all.
4. Keep the manual detailed and coherent: full coverage of the current process, a comfortable reading sequence, and the rule that it grows in the same commit as the project — new tooling included.

## Status

- [x] ADR-0006 + ADR-0007 created through the generator (**proposed** — acceptance is the owner's)
- [x] `docs/development/conventions/process.md` — the two phases, the review, statuses, DoR
- [x] `docs/development/process.md` — walkthrough reordered (Plan/Slice before the review); example ADR number `0006` → `0008`
- [x] `docs/development/repository.md` — second-level map incl. the `.agents/` layers; the `toolchain.md` layout table folded in
- [x] `docs/development/working-with-agents.md` — the agents chapter; renamed from `agents.md` at the owner's direction so the write gate never blocks its edits; carries the `Where to next` block and a naming-constraint note (protected basenames, so the name is not "corrected" back)
- [x] satellites: specs README + guide + templates, `spec_check.py` (plan/tasks required from *Approved*), glossary, getting-started, manual README + root README, agent-side skill / command / eval, `memory.md`
- [x] gates: `doit verify` (links 49 + 156 resolved, tree 24/24) / `doit docs_check` / `doit trace` — all green after the rename
- [x] completeness + coherence pass: `Where to next` chain through the chapters (getting-started → repository → toolchain → workflows → process → agents → documentation guides → conventions → glossary); living-document rule in the Documentation System (DoD rows for tools and directories) and in the manual README; two overpromising phrases fixed (`install notes` → `versions and paths`)
- [x] rename sweep: all 9 references updated across 7 files (root README, manual README, `repository.md`, `process.md` ×2, `workflows.md`, `conventions/process.md`, ADR-0007 ×2) + `memory.md` and this file; no `claude.md` / `soul.md` / `.cursorrules` anywhere in the tree; the only `AGENTS.md` is the root one

## Discovered Issues

- The walkthrough's fictional ADR number (`ADR-0006`) collided with the two real new records — the example moves to `ADR-0008`.
- `.kilo/worktrees/hip-humerus` is a stale local worktree copy of the repository — not touched.
- `AGENTS.md` (root) left untouched: the new material lives in the manual; its Process bullet stays accurate.
- The `Where to next` addition to the agents chapter was blocked by the protected-file guard — the basename `agents.md` is in the harness's always-ask set (`agents.md` / `claude.md` / `soul.md` / `.cursorrules`, any directory, case-insensitive; verified in the harness's write-guard module; no extra config patterns). **Resolved**: the owner directed the rename — the chapter is now `working-with-agents.md`; the constraint note in the chapter keeps the name from being "corrected" back.

## Next action

Await the owner's review of the change set; commit only on an explicit request. If the owner accepts, ADR-0006 and ADR-0007 move from *proposed* to *accepted* — a status move only the owner makes.
