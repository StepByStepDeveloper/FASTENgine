# Policies / Guardrails

Prohibitive barriers, not style rules: what an agent working in this repository must never do. Naming, formatting and documentation conventions live in [`docs/development/conventions/`](../../docs/development/conventions/style.md); this file holds the actions a rule cannot undo after the fact.

**Status**: active. The list is binding; extend it as new hazards appear rather than growing the rules docs.

## Prohibited

- NEVER write a credential, token, private key or `.env` value into any file of this repository.
- NEVER commit, amend, rewrite history or push on your own initiative — commits happen only when the owner asks for them, and then as one atomic, focused change.
- NEVER run a destructive git operation (`push --force`, `reset --hard` over published history, history rewriting, deleting a branch you did not create) without an instruction that names the operation.
- NEVER modify third-party, vendored or generated code (`vcpkg_installed/`, generated bindings): it is never documented, never reformatted and never patched — see the `Exceptions` section of [`../../docs/development/conventions/style/documentation.md`](../../docs/development/conventions/style/documentation.md).
- NEVER resolve an unclear requirement by assumption. The `Ambiguity` core rule of `AGENTS.md` outranks progress: stop and ask.
- NEVER weaken a rule, an example or a check to make a verification pass. Fix the artifact the rule governs, or report the conflict.
- NEVER leave a placeholder, a dead reference or an empty block where an artifact is required — placeholders are reported as findings, not filled in by guessing (see the `Prohibited` section of [`../../docs/development/conventions/style/documentation.md`](../../docs/development/conventions/style/documentation.md)).
- NEVER implement a feature before its specification is *Approved*, and never move a specification's status (Draft / Approved / Implementing / Implemented / Superseded) on your own initiative — that word is the owner's (see [Process](../../docs/development/conventions/process.md)).
- NEVER skip the red step: a task's test is written and shown failing before any implementation code, and the failing run is quoted, not described.
- NEVER modify, weaken or disable an existing test to reach green. A failing existing test is evidence: report it with its output and let the owner decide which side is wrong.
- NEVER let behaviour drift from the specification: when what is built differs from what is written, one of the two is corrected in the same change, and the owner decides which.

## Escalation

A prohibited action that has already happened is reported, not silently repaired: state what happened, in which file, and what the safe repair is, then wait for the owner's decision.
