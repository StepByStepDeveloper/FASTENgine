---
description: "Add or change a rule in .agents/rules without breaking the tree"
argument-hint: "<topic>"
---

Add the rule about `<topic>` to the rules tree, following the discipline the existing documents already follow:

1. **One home for the grammar.** A rule is stated once, in the section that owns it; a later section points at it with an anchor instead of restating it.
2. **Five homes for a convention.** A new convention appears in its table row, in the normative notice that explains it, in the exception section it names, in a compiled example, and in that example's "this example covers" list.
3. **Discoverability.** Wire a new document into the area index (`.agents/rules/style.md`), into `AGENTS.md` as a core-rule bullet when it is mandatory for every created artifact, and into each sibling document that governs the same artifacts.
4. **Collateral contradictions.** Search the tree for artifacts the new rule now contradicts — deliberately uncommented reference examples, sample snippets — and give each an explicit exemption note or bring it into compliance.
5. **Verify, then stop.** Run `.agents/skills/verify-rules/`, report what passed and what stays open, and leave the diff uncommitted: commits happen on an explicit request.
