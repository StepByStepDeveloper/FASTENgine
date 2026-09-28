---
description: "Commit the staged work as one focused change, the way this repository commits"
---

**Status**: active — the prompt is usable today; the commit conventions it applies live in [Git & PR Workflow](../rules/git.md).

Commit the current work following the repository's own conventions:

1. **Only on an explicit request.** Commits happen when the owner asks for them — never on your own initiative, and never as a side effect of another task (see [Policies / Guardrails](../policies/guardrails.md)).
2. **One theme per commit.** If the working tree mixes themes, say so and ask which one to commit; do not split the batch by hand without a decision.
3. **Verify first, quote the evidence.** Run `doit verify` and the build and tests the change touches; the message body carries what was run and what it returned.
4. **Message.** Conventional Commits, English, imperative mood, one theme — `docs:`, `feat:`, `fix:`, `refactor:`, `chore:`. A long body names what changed, why, and the verification evidence the repository's own commits carry.
5. **Stage the whole theme.** Include the artifacts the change produced — a new document, its index line, the example it demonstrates — and nothing else.
6. **Report, then stop.** Name the commit subject, the files, the evidence and what stays open. Pushing is a separate request.
