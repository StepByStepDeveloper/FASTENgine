# Process (SDD + ADR + TDD)

How a change becomes a merged, verified state in FASTENgine: the specification-driven loop, the decision records that anchor it and the test-driven implementation that closes it. This rule is binding for every non-trivial change; the walkthrough with a worked example is [The development process](../process.md), and every artifact named here has a home in [The repository](../repository.md).

**Status**: active — adopted by ADR-0005; the pilot feature will be the first run of the loop.

## The workflow

Every non-trivial change walks five stages; each stage leaves one artifact behind:

| Stage | Artifact | Home | Gate |
|:--|:--|:--|:--|
| 1. Specify | `spec.adoc` | `docs/specs/NNN-<slug>/` | `doit spec_check`; *Approved* by the owner |
| 2. Decide | ADR, when a decision is at stake | `docs/arc42/adr/` | `doit docs_check`; created through `tools/new_adr.py` |
| 3. Plan | `plan.adoc` | the spec directory | reviewed together with its ADRs |
| 4. Slice | `tasks.adoc` | the spec directory | every task covers at least one criterion |
| 5. Implement | code and tests | `src/` | the TDD loop below; `doit trace` |

A change may skip a stage only by the proportionality table at the end of this document; skipping is a decision, never an accident.

## Specifications

- One feature — one specification, one to three pages; a specification that outgrows three pages is two features.
- Home and naming: `docs/specs/NNN-<slug>/`, numbered from 001; the directory number is the feature's number everywhere — in the title, in every identifier, in the tasks.
- The templates live in `docs/specs/_templates/`; copy them. The writing guide is [Specifications](../documentation/specs.md).
- Identifiers — `FR-NNN-ii`, `NFR-NNN-ii`, `AC-NNN-ii`, `T-NNN-ii` — are stable addresses that tests and code point at. They are never reused; a removed requirement is marked `(withdrawn)` in place, not deleted.
- Every functional requirement is written in EARS form; every acceptance criterion is checkable and names its requirement in parentheses (Given/when/then; `Verification: automated`, or `manual` with the reason).
- The status line moves left to right only:

| Status | Means | Set by | What `spec_check` enforces |
|:--|:--|:--|:--|
| Draft | being written; `NEEDS CLARIFICATION` allowed | author | template shape |
| Approved | the promise: requirements, criteria and ADRs settled | owner (human) | completeness, no open questions |
| Implementing | plan and tasks exist; the loop runs | author | plan and tasks present |
| Implemented | all criteria covered; the definition of done met | owner (human) | — (`doit trace` covers this) |
| Superseded | replaced by a later specification | owner | — |

- The owner approves; the agent drafts. An agent never moves a specification to *Approved* or *Implemented*.

## Definition of Ready

Implementation may start when every line holds:

- [ ] The specification is *Approved* and carries no `NEEDS CLARIFICATION`.
- [ ] Every acceptance criterion is checkable by a test (or explicitly manual, with the reason).
- [ ] The decisions the feature needs have accepted ADRs.
- [ ] The plan is agreed; the tasks are sliced.

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

A red gate stops the change: fix the artifact, not the gate.

## Roles

- **Owner** (the maintainer): approves specifications, accepts ADRs, approves changes to existing tests — the only human authority in the loop.
- **Author**: writes the specification, walks the statuses, implements under TDD.
- **Agent**: drafts specifications and ADRs, writes tests and code, keeps plan, tasks and statuses current — never approves its own work.
- **Reviewer** (human, or the personas under `.agents/agents/`): checks the trace specification -> test -> code and the absence of drift.

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
| One process size for everything | The proportionality table |
| The coverage number as the goal | Traceability, not coverage, is the measure |

## Maintenance

- On every release: walk the specifications in *Implementing* — stalled features; risks and debt go into arc42 §11.
- Quarterly: process review — what slowed the loop, what was skipped; retire stale drafts; confirm the ADR set still reflects reality.
- Agent retrospectives: a repeated agent mistake updates the skills, guardrails and templates — through the admission test in [`.agents/rules/README.md`](../../../.agents/rules/README.md).
