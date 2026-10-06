---
description: "Draft a feature's specification from a request — questions first, template-filled, stopping at approval"
---

**Status**: active — applies [Process](../../docs/development/conventions/process.md) through the `write-spec` skill.

Draft a specification for the feature described below.

1. **Questions first.** Do not write code, and do not invent scope. Ask the owner whatever is unclear; mark every unresolved point as `NEEDS CLARIFICATION` in place.
2. **Follow the template.** `docs/specs/_templates/spec.adoc`, copied to `docs/specs/NNN-<slug>/`. Requirements in EARS form with IDs; every acceptance criterion given/when/then and checkable, or marked `manual` with the reason; Non-goals listed.
3. **Ground it.** Check `AGENTS.md`, the ADRs in `docs/arc42/adr/` and arc42 sections 1–3 and 5 for constraints — link them, never copy them.
4. **Stop at the review.** The package — specification, plan, tasks — is presented to architectural review and feature planning; only the owner approves. Draft `plan.adoc` and slice `tasks.adoc` before presenting (same skill).
5. **Gate.** `doit spec_check` after every edit; report what it says, verbatim.

Feature request:
<paste>
