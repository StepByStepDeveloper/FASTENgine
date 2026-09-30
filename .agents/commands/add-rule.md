---
description: "Add or change a rule under its proper home without breaking the tree"
argument-hint: "<topic>"
---

**Status**: active — the prompt is usable today; the discipline it applies lives in the existing documents.

Add the rule about `<topic>` under its proper home, following the discipline the existing documents already follow:

1. **Route it first.** One home per rule, never two: a rule with a human reader goes to the development conventions; an agent-only standing rule goes to [`.agents/rules/`](../rules/README.md) and must pass its admission test first; a prohibition goes to `policies/guardrails.md`; what a gate, hook or formatter can enforce is enforced there; a task-shaped procedure is a skill, and a named prompt is a command.
2. **One home for the grammar.** A rule is stated once, in the section that owns it; a later section points at it with an anchor instead of restating it.
3. **Five homes for a convention.** A new convention appears in its table row, in the normative notice that explains it, in the exception section it names, in a compiled example, and in that example's "this example covers" list.
4. **Discoverability.** Wire a new document into the conventions index (`docs/development/conventions/README.md`) and the style area index (`docs/development/conventions/style.md`), into `AGENTS.md` as a core-rule bullet when it is mandatory for every created artifact, and into the `AGENTS.md` router table when it is a new `.agents/` artifact; add it to each sibling document that governs the same artifacts.
5. **Collateral contradictions.** Search the tree for artifacts the new rule now contradicts — deliberately uncommented reference examples, sample snippets — and give each an explicit exemption note or bring it into compliance.
6. **Verify, then stop.** Run `.agents/skills/verify-rules/`, report what passed and what stays open, and leave the diff uncommitted: commits happen on an explicit request.
