---
description: "Execute one task from tasks.adoc through red, green and refactor, with the evidence shown"
---

**Status**: active — applies [Process](../../docs/development/conventions/process.md) through the `tdd-cycle` skill.

Implement T-NNN-xx from `docs/specs/NNN-<slug>/tasks.adoc`.

1. Read only the task, its FR/AC, the relevant plan part and the ADRs it touches.
2. If anything is unclear, stop and ask.
3. **Red**: add the minimal API stub so the test compiles, write the failing test (`@brief`, `@covers{AC-...}`), run the target, show the failing output — then stop for the owner's approval of the test.
4. **Green**: the minimum code to pass; run the target and show the output.
5. **Refactor** without changing behaviour; run `bazel test //...`.
6. Complete the Doxygen contracts (`@implements{FR-...}` where the link is not obvious; pre/post, ownership, thread-safety).
7. `doit trace`; set the task row to `done`; report changed files, the test outputs, and any deviation from the plan.

Prohibited: modifying or disabling existing tests, changing the public API outside the task, adding dependencies, widening scope.

Task: T-NNN-xx
