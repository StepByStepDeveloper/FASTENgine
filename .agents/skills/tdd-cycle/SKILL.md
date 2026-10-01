---
name: tdd-cycle
description: "Implement one task from tasks.adoc test-first — red, green, refactor, then the trace gate. Use when executing a task, showing a red step, or moving a task to done."
---

# Run the TDD Cycle

One task, one behavior, one test — from `tasks.adoc` of an *Implementing* specification to a `done` row and a clean trace. The binding rules are [Process](../../../docs/development/conventions/process.md); the quality bar is [Testing](../../../docs/development/conventions/testing.md).

**Status**: active — the loop is the repository's implementation procedure; sanitizer configurations arrive with the first sources.

## When to Use

- Executing the next `todo` row of a specification's `tasks.adoc`.
- Re-doing a change that skipped the red step: the failure is reproduced first, then fixed.
- Don't use for: spikes (time-boxed experiments, thrown away after the answer) or documentation-only changes.

## Procedure

1. **Read only what the task needs**: the task row, its FR/AC, the relevant plan section, the ADR it touches. Do not read ahead.
2. **Unclear anything? Stop and ask.** Never fill a requirement gap with invention.
3. **Red.** Add the minimal API stub so the test compiles, then the test: a Doxygen block with `@brief` and `@covers{AC-NNN-ii}`. Run the target and show the failure — it must fail for the behavioural reason, not a missing symbol. Then stop: test changes are the owner's decision, so the new test is approved before implementation.
4. **Green.** Minimal code that passes; run the target; show the output. Run the whole suite before marking done — nothing else may break.
5. **Refactor** without changing behaviour; run the suite again.
6. **Complete the contracts.** `@implements{FR-NNN-ii}` on the realizing entity when the link is not obvious from its Doxygen group; pre/post conditions, ownership and thread-safety in the block per [Documentation (Doxygen)](../../../docs/development/conventions/style/documentation.md).
7. **Close the task.** `doit trace` clean; the task row moves to `done`; behaviour that deviated from the specification is updated in the specification in the same change (with approval).
8. **Report** — changed files, the red output and the green output, and any deviation from the plan.

## Pitfalls

- **A test that cannot fail for the right reason.** Without a stub it fails at link time; that is not a red step.
- **Weakening an existing test to reach green.** Forbidden — an existing test fails because the change is wrong, or because the contract is genuinely changing, and that is the owner's decision.
- **Silence over coverage.** A criterion no test covers is `doit trace`'s problem to report and yours to fix — by a test, or by a plan change, never by removing the criterion.
- **Concurrency shortcuts.** Repeat concurrency tests and keep ThreadSanitizer clean once the configurations exist; a reported race is a red step.

## Verification

The red run and the green run are both shown; the target passes under `bazel test`; `doit trace` reports no problems for the specification.
