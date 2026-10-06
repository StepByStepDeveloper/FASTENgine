---
name: write-spec
description: "Draft or maintain a specification package under docs/specs/ — spec.adoc, plan.adoc, tasks.adoc. Use when a feature is specified, planned, re-planned or sliced into tasks."
---

# Write a Specification

How a feature becomes three reviewable artifacts under `docs/specs/NNN-<slug>/`. The binding rules are [Process](../../../docs/development/conventions/process.md); the writing guide is [Specifications](../../../docs/development/documentation/specs.md); the templates are `docs/specs/_templates/`.

**Status**: active — the templates, the writing guide and the gates (`doit spec_check`, `doit trace`) exist; the first pilot feature will exercise them end to end.

## When to Use

- A new feature is requested: draft the planning package — `spec.adoc`, then `plan.adoc` and `tasks.adoc`.
- An approved package is picked up for implementation and needs re-planning, or its tasks must follow a change.
- Requirements changed and the specification must follow — in the same change as the code.
- Don't use for: bug fixes and refactors that restore intended behaviour — those are test-first, no specification.

## Procedure

1. **Copy the templates** — never write into `_templates/` itself:
   ```bash
   cp -r docs/specs/_templates docs/specs/NNN-<slug>
   ```
2. **Draft `spec.adoc` top to bottom.** Goal, Context, Non-goals, Requirements, Acceptance criteria, Constraints, Open questions, Links. Requirements in EARS form (`FR-NNN-ii`, `NFR-NNN-ii`); criteria given/when/then, each naming its requirement (`AC-NNN-ii`). Do not write code.
3. **Ask before assuming.** Anything unclear becomes a question to the owner, and every unresolved point stays written as `NEEDS CLARIFICATION` in place. Check `AGENTS.md`, the ADR set and arc42 sections 1–3 and 5 for constraints; link, never copy.
4. **Stop at the review.** Only the owner moves the status to *Approved*, at architectural review and feature planning — you present the whole package, never approve it. Ask for it only when: no `NEEDS CLARIFICATION` remains, every criterion is checkable, the decisions the feature needs are settled as ADRs (prepare drafts with the `write-adr` skill; never accept them yourself), and the plan and the tasks are drafted.
5. **Write `plan.adoc`** before the review: approach, affected building blocks, public API sketch, data and concurrency model, performance considerations, test strategy (criteria to tests mapping), risks — and every decision that still needs an ADR, drafted but not accepted.
6. **Slice `tasks.adoc`**: one row, one behavior, one test, its `Covers` criterion and its Bazel target. The status column is `todo` / `doing` / `done` / `withdrawn`; keep it current while implementing.
7. **Gate after every edit:** `doit spec_check`. From *Approved* onward it enforces completeness and requires the plan and the tasks; the coverage side is `doit trace` once tests exist.

## Pitfalls

- **Placeholders survive.** `NNN` and `<angle brackets>` are tolerated only while the status is `Draft`; they become failures at approval.
- **Restating instead of linking.** Architecture facts live in arc42; the specification links with `arc42: <section>` and moves on.
- **Reusing identifiers.** `FR- / NFR- / AC- / T-` identifiers are permanent addresses; a withdrawn item is marked, never renumbered into reuse.
- **Status drift.** Implementing an unapproved specification, or reaching *Implemented* with uncovered criteria, is exactly what the gates refuse; fix the artifact, never the gate.

## Verification

`doit spec_check` exits 0 with no problems at the current status; `doit trace` is clean once tasks name real targets.
