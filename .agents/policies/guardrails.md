# Policies / Guardrails

Prohibitive barriers, not style rules: what an agent working in this repository must never do. Naming, formatting and documentation conventions live in [`../rules/`](../rules/style.md); this file holds the actions a rule cannot undo after the fact.

**Status**: active. The list is binding; extend it as new hazards appear rather than growing the rules docs.

## Prohibited

- NEVER write a credential, token, private key or `.env` value into any file of this repository.
- NEVER commit, amend, rewrite history or push on your own initiative — commits happen only when the owner asks for them, and then as one atomic, focused change.
- NEVER run a destructive git operation (`push --force`, `reset --hard` over published history, history rewriting, deleting a branch you did not create) without an instruction that names the operation.
- NEVER modify third-party, vendored or generated code (`vcpkg_installed/`, generated bindings): it is never documented, never reformatted and never patched — see the `Exceptions` section of [`../rules/style/documentation.md`](../rules/style/documentation.md).
- NEVER resolve an unclear requirement by assumption. The `Ambiguity` core rule of `AGENTS.md` outranks progress: stop and ask.
- NEVER weaken a rule, an example or a check to make a verification pass. Fix the artifact the rule governs, or report the conflict.
- NEVER leave a placeholder, a dead reference or an empty block where an artifact is required — placeholders are reported as findings, not filled in by guessing (see the `Prohibited` section of [`../rules/style/documentation.md`](../rules/style/documentation.md)).

## Escalation

A prohibited action that has already happened is reported, not silently repaired: state what happened, in which file, and what the safe repair is, then wait for the owner's decision.
