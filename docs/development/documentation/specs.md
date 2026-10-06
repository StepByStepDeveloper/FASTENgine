# Specifications

How to write and maintain the artifacts under `docs/specs/`. This is the writing guide; the binding rules — statuses, permissions, gates — are [Process (SDD + ADR + TDD)](../conventions/process.md), and the layout is described in its README (`docs/specs/README.adoc`). Where this guide and the convention disagree, the convention wins.

## What a specification is — and is not

A specification is the **contract of intent** for one feature: what is being built, for whom, and how the result will be verified. It is written and agreed before any code — the review sees the whole planning package — and kept current after the code: it is the one document that stays true across the feature's whole life.

It is *not*:

- a design document — the *how* lives in `plan.adoc`;
- an architecture statement — the system's shape lives in arc42, and the specification links to it;
- a decision record — a choice with alternatives becomes an ADR, and the specification references it;
- a test plan — the test strategy belongs to the plan, and the tests themselves carry their anchors.

One feature, one specification, one to three pages. A specification that outgrows three pages is usually two features; splitting early is cheaper than splitting later.

## The three files

| File | Answers | Written |
|:--|:--|:--|
| `spec.adoc` | What are we building, and how will we know it works? | first, in the planning phase |
| `plan.adoc` | How will we build it? | with the specification, before the review |
| `tasks.adoc` | In what order, one behavior at a time? | after the plan, still before the review |

They live together in `docs/specs/NNN-<slug>/` and are copied from `docs/specs/_templates/`. The identifiers inside them — `FR-NNN-ii`, `NFR-NNN-ii`, `AC-NNN-ii`, `T-NNN-ii` — are permanent addresses: tests and code point at them, `doit trace` counts them, and they are never reused, even after the requirement is withdrawn.

## Writing `spec.adoc`

**Goal.** Why this feature exists, for whom, in three to five sentences. This is the paragraph a reader keeps in mind through everything else — write it last if that helps, but do not leave it vague.

**Context.** The background a reader needs: the building blocks it touches, the arc42 sections and ADRs it relates to. Link, do not copy — a restated architecture fact goes stale in two places instead of one.

**Non-goals.** What a reader could reasonably expect but will not get. Non-goals are the cheapest scope control there is.

**Requirements.** Functional requirements are numbered and written in EARS form — the five patterns are tabulated in [The development process](../process.md). The shape of a good requirement: one behavior per line, no "and", no implementation nouns, a response you could observe. Non-functional requirements must be measurable and name their measurement conditions; "fast" is not a requirement, "wait-free for the producer on the reference configuration" is.

**Acceptance criteria.** One line per criterion, given/when/then, naming the requirement it discharges in parentheses, stating the observable result. Criteria are what tests are written against and what `doit trace` counts — a criterion that no test can embody is a requirement not yet understood.

**Constraints.** Standards, platforms, dependencies, performance budgets, links to the ADRs that carry the decisions.

**Open questions.** Every open point is spelled `NEEDS CLARIFICATION` in place. The marker is a gate: approval flips it from a note into a problem. When a question is resolved, rewrite the line as the answer — do not leave resolved questions lying around as history.

**Links.** The pointers out: plan, tasks, ADRs, the Doxygen group, the eventual test targets.

## Writing `plan.adoc`

The plan is reviewed with the ADRs and is allowed to be technical — signatures, ownership, threading. Its sections: Approach; Affected building blocks; Public API sketch (signatures only — the contract the plan commits to); Data and concurrency model; Performance considerations; Decisions requiring an ADR; Test strategy (levels, doubles, benchmarks, sanitizers, and the AC-to-tests mapping); Risks. If writing the plan surfaces a decision between real alternatives, it becomes an ADR — the plan cites it and moves on.

## Writing `tasks.adoc`

One row, one behavior, one test. A task that needs the word "and" in its description is two tasks; a task whose "Covers" cell names no acceptance criterion does not belong in the list. The Bazel target column is where the test will live, so the task list doubles as a map of the test suite before it exists. Status is `todo`, `doing`, `done`, or `withdrawn`; the file is the status board for the feature — keep it current as you go, not at the end.

## Checklists

**A good specification:**

- [ ] Goal is readable without any other document; Context links instead of restating.
- [ ] Every functional requirement is one EARS statement; every non-functional one is measurable.
- [ ] Every requirement has at least one acceptance criterion; every criterion names its requirement.
- [ ] Every criterion is checkable by a test, or marked `manual` with the reason.
- [ ] No `NEEDS CLARIFICATION` remains at approval; withdrawn items are marked, not deleted.
- [ ] Identifiers are unique within the specification; nothing reuses a retired number.
- [ ] The header names the ADRs and arc42 sections the feature touches.

**A good acceptance criterion:**

- [ ] States inputs and observable outcome — not the implementation that achieves it.
- [ ] Fails for exactly one reason when unmet.
- [ ] Passes when the requirement is met, even if the implementation is replaced wholesale.

**A good task list:**

- [ ] One behavior per row; one test per row.
- [ ] Every criterion is covered by at least one task.
- [ ] Every row names its Bazel target where the test will live.
- [ ] The order is an implementation order, not a wish list.

## Common mistakes

| Mistake | What it looks like | Fix |
|:--|:--|:--|
| Kitchen-sink spec | three features in one file; four pages and growing | split by feature; three pages is the ceiling |
| The criterion that repeats the requirement | AC restates the FR word for word | state the observable scenario — inputs, action, outcome |
| The criterion that prescribes | AC names a class, a function or a data structure | describe behavior; the plan carries the names |
| Restated architecture | Context explains the system instead of linking arc42 | link, never copy |
| Open question in prose | a question without the `NEEDS CLARIFICATION` marker | use the marker; the gate cannot see prose |
| The task list as a diary | rows for "investigate", "clean up" | tasks are behaviors; investigation is a spike, recorded in the plan |
| Late anchors | `@covers` added after the feature ships | the anchor is written with the test, in the red step — see [Testing](../conventions/testing.md) |

## Where to next

- [Process (SDD + ADR + TDD)](../conventions/process.md) — statuses, approval, the gates.
- [Decision records](adr.md) — the companion artifact for decisions.
- [The development process](../process.md) — the walkthrough that uses these files end to end.
