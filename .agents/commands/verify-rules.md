---
description: "Run the specification gate (context tree + conventions) and report each run's result"
---

**Status**: active — the prompt is usable today; the sweep it invokes is defined in [`.agents/skills/verify-rules/SKILL.md`](../skills/verify-rules/SKILL.md).

Run the full sweep defined in `.agents/skills/verify-rules/SKILL.md` — the compilers, the standards and the heading gate are that skill's, so take them from there rather than from this file — and report:

- the exit code of every run;
- each compiler with the version actually used;
- every warning you did not expect.

Report first; fix only when asked to.
