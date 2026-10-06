# Process (SDD + ADR + TDD)

How a change becomes a merged, verified state in FASTENgine: the specification-driven loop, the decision records that anchor it and the test-driven implementation that closes it. The process serves developers first — every stage is a command or a document a person carries alone, and an agent is an optional assistant under the same rules ([Working with agents](../working-with-agents.md)), never a requirement. This rule is binding for every non-trivial change; the walkthrough with a worked example is [The development process](../process.md), and every artifact named here has a home in [The repository](../repository.md).

**Status**: active — adopted by ADR-0005; extended with the planning/implementation split (ADR-0006) and the developer-first rule (ADR-0007); the pilot feature will be the first run of the loop.

## The two phases

The process separates, in logic and in time, two activities that used to move as one:

| Phase | Produces | Ends with |
|:--|:--|:--|
| Architectural and feature planning | the planning package of one or more features: `spec.adoc`, `plan.adoc`, `tasks.adoc`, the ADRs the decisions need | agreement at the **architectural review and feature planning** |
| Implementation | code, tests, documentation updates | the definition of done of the feature |

Several authors — architects included — may prepare packages in parallel, and one review may agree a whole batch of them. An *Approved* specification is the agreed backlog: implementation starts when a team picks it up, possibly long after, possibly by different people than planned. Planning running ahead of implementation is the normal mode, not a special case.

## The workflow

Every non-trivial change walks six stages; the table names each stage's artifact and its gate:

| Stage | Artifact | Home | Gate |
|:--|:--|:--|:--|
| 1. Specify | `spec.adoc` | `docs/specs/NNN-<slug>/` | `doit spec_check` — the draft shape |
| 2. Decide | ADR, when a decision is at stake | `docs/arc42/adr/` | `doit docs_check`; created through `tools/new_adr.py` |
| 3. Plan | `plan.adoc` | the spec directory | reviewed with its ADRs |
| 4. Slice | `tasks.adoc` | the spec directory | every task covers at least one criterion |
| 5. Agree | the status *Approved* — the review's outcome | the spec directory | the owner approves at the review; from here `spec_check` treats open points as failures and requires the plan and the tasks |
| 6. Implement | code and tests | `src/` | the TDD loop below; `doit trace`; starts when a team picks the package up |

Stages 1–4 are the planning phase; stage 5 is its review; stage 6 is the implementation phase. A change may skip a stage only by the proportionality table at the end of this document; skipping is a decision, never an accident.

## The architectural review and feature planning

The agreement gate has two halves; they may be held together or apart:

- **Architectural review** examines the package as architecture: requirements in EARS form, criteria a test can embody, ADRs that settle the decisions, a plan that commits to something buildable.
- **Feature planning** places the package: priority, the team or developer who will implement it, and when. Deferred work is scheduled into an implementation phase here — or left waiting as an *Approved* item.

The outcome is recorded the only way this process records anything: in the statuses. The owner moves the specification to *Approved* and accepts the ADRs the package rests on; the review is the moment a specification stops being prose and becomes a promise. A package with an open point is not approved — the gap goes back to its author.

## Specifications

- One feature — one specification, one to three pages; a specification that outgrows three pages is two features.
- Home and naming: `docs/specs/NNN-<slug>/`, numbered from 001; the directory number is the feature's number everywhere — in the title, in every identifier, in the tasks.
- The templates live in `docs/specs/_templates/`; copy them — all three, as one package. The writing guide is [Specifications](../documentation/specs.md).
- Packages may be authored in parallel: one feature — one specification directory keeps them independent, and identifiers carry the specification's number, so two authors cannot collide.
- Identifiers — `FR-NNN-ii`, `NFR-NNN-ii`, `AC-NNN-ii`, `T-NNN-ii` — are stable addresses that tests and code point at. They are never reused; a removed requirement is marked `(withdrawn)` in place, not deleted.
- Every functional requirement is written in EARS form; every acceptance criterion is checkable and names its requirement in parentheses (Given/when/then; `Verification: automated`, or `manual` with the reason).
- The status line moves left to right only:

| Status | Means | Set by | What `spec_check` enforces |
|:--|:--|:--|:--|
| Draft | being written; the planning package takes shape; `NEEDS CLARIFICATION` allowed | author | template shape |
| Approved | the promise: agreed at the review; waits as the backlog for its team | owner (human), at the review | completeness, no open questions; plan and tasks present |
| Implementing | picked up; the loop runs | author | plan and tasks present |
| Implemented | all criteria covered; the definition of done met | owner (human) | — (`doit trace` covers this) |
| Superseded | replaced by a later specification | owner | — |

- The owner approves; the author — a developer or an agent — never approves their own package, and an agent never moves a specification to *Approved* or *Implemented*.

## Definition of Ready

Implementation may start when every line holds:

- [ ] The specification is *Approved* — agreed at architectural review and feature planning — and carries no `NEEDS CLARIFICATION`.
- [ ] Every acceptance criterion is checkable by a test (or explicitly manual, with the reason).
- [ ] The decisions the feature needs have accepted ADRs.
- [ ] The package is current: the plan and the tasks still describe the work — a package that waited is walked through this checklist again before its first task, and a stale one goes back through the review, not around it.

## Definition of Done

A feature is done when every line holds:

- [ ] Every acceptance criterion is covered by a test; `doit trace` is clean.
- [ ] `doit` (verify + build + test) and `doit docs` are green.
- [ ] Sanitizers are clean for the code the feature touched.
- [ ] Doxygen builds without warnings for the new code; the contracts it documents match the specification.
- [ ] The specification is updated and set to *Implemented*.
- [ ] arc42 (§5, §6, §8, §10, §11) and the ADRs (§9) describe the feature as built.
- [ ] No existing test was weakened or deleted without the owner's approval.

## The TDD loop

Implementation is the second phase: it may begin right after the review or much later, possibly by a different team than the one that planned the feature. The loop itself is fixed:

- The unit of work is one task from `tasks.adoc`: one behavior, one test, one passing commit.
- Red first: the failing test is written and its output is shown before any implementation exists — the failure is behavioral (an API stub compiles), never a missing symbol.
- Green: the smallest change that makes the test pass; no code without a failing test behind it.
- Refactor under green: behavior stays put, structure improves; run the full suite, not just the touched target.
- The test quality bar and the mechanics live in [Testing](testing.md); the practice not negotiable here: tests before code, and tests are strengthened — never weakened — as behavior changes.

## Traceability

- Two aliases tie the three layers together: tests carry `@covers{AC-NNN-ii}`, implementation names `@implements{FR-NNN-ii}` where the link is not obvious from its Doxygen group. Both are Doxygen aliases, defined in `docs/api/Doxyfile`.
- `doit trace` writes the report into `build/trace/`: covered and uncovered criteria per specification, references that name nothing, and the sources scanned. An *Implemented* specification with an uncovered criterion fails the report.
- Requirement text is not retyped anywhere: arc42, the ADRs and the specifications cross-reference identifiers instead of copying prose.

## Change control

- The specification is the contract of *intent*: when the feature turns out different, the specification changes in the same commit as the code, so the difference is visible in the diff.
- A change that alters a decision worth recording takes an ADR first; a change of wording alone does not.
- A superseded specification stays on disk with the status flipped and identifiers untouched.
- An accepted ADR is immutable in substance — a changed decision becomes a new ADR that supersedes the old one, per [Documentation system](docs.md).

## Gates and who runs them

| Gate | Runs on | Where |
|:--|:--|:--|
| `doit spec_check` | staged `docs/specs/` changes, CI | part of `doit verify`; the pre-commit hook |
| `doit trace` | CI; before a feature is declared done | report into `build/trace/` |
| `doit` and `doit docs` | before every pull request | local; CI |
| The PR checklist | every pull request | `.github/pull_request_template.md` |

A red gate stops the change: fix the artifact, not the gate. The blocking checkpoint is CI (and the secret scan locally); the pre-commit tree checks are advisory for now — they warn, and `--no-verify` bypasses them entirely — so a local red is an early failure, never a lighter one.

## Roles

- **Owner** (the maintainer): approves specifications — at the review — accepts ADRs, approves changes to existing tests — the only human authority in the loop.
- **Author**: authors the planning package, walks the statuses, implements under TDD; the planning author and the implementing team may be different people.
- **Architect**: an author in the planning phase — one of possibly several preparing packages in parallel; the role ends at the review.
- **Agent**: drafts specifications and ADRs, writes tests and code, keeps plan, tasks and statuses current — never approves its own work. Optional everywhere: every stage above is doable by hand.
- **Reviewer** (human, or the personas under `.agents/agents/`): checks the trace specification -> test -> code, and at the review events the package as a whole.

## Proportionality

| Change | What the process demands |
|:--|:--|
| Typo, comment, formatting | The change itself; the gates as usual. |
| A fix or a small helper | A failing test first, then the fix, one PR; no specification, no ADR. |
| A feature | The full loop above, from specification to definition of done. |
| Cross-cutting (public API, concurrency model, build) | The full loop, an ADR before implementation, and a spike when feasibility is in question. |

## Failure modes this process is built against

| Failure | The rule that answers it |
|:--|:--|
| Specification and code drift apart | Change control; `spec_check`; `doit trace` |
| Tests written after the code | The red step is visible in the PR |
| A test weakened to reach green | Existing tests change only with the owner's approval |
| Oversized tasks | One task — one behavior — one test |
| An ADR written in hindsight | Decisions are a plan item, not a postmortem |
| Implementation and planning artificially coupled — one waits on the other | The two phases; the review gate; the *Approved* backlog |
| A package stale by the time a team picks it up | The Definition of Ready re-check; a stale package goes back through the review |
| One process size for everything | The proportionality table |
| The coverage number as the goal | Traceability, not coverage, is the measure |

## Maintenance

- On every release: walk the specifications in *Implementing* — stalled features; risks and debt go into arc42 §11. Walk the *Approved* backlog with feature planning: packages whose plan went stale are re-reviewed or retired.
- Quarterly: process review — what slowed the loop, what was skipped; retire stale drafts; confirm the ADR set still reflects reality.
- Agent retrospectives: a repeated agent mistake updates the skills, guardrails and templates — through the admission test in [`.agents/rules/README.md`](../../../.agents/rules/README.md).
