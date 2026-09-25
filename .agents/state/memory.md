# MEMORY — project knowledge that outlives a session

Knowledge about *this repository* that a fresh session cannot re-derive cheaply. Entries are added, never rewritten in place; each names where it applies, and the list is reviewed by hand for staleness.

**Status**: active. Not to be confused with the agent's own memory (which is profile-scoped and lives outside the repository, in Hermes) or with [`scratchpad.md`](scratchpad.md) (which dies with the task).

## Architecture Pitfalls

- `style/naming.md` is deliberately **project-agnostic**: it is seasoned on this project and staged for extraction into its own repository. Its disagreement with `style/patterns.md` — interface and protocol role markers are built on virtual functions, which the project's own patterns forbid — is therefore expected, not a defect to repair. Editing either side is the owner's call.
- The rules tree is verified mechanically by the [`verify-rules` skill](../skills/verify-rules/SKILL.md): **green** means every run that skill defines exits 0 — the matrix itself lives there, not here.
- Every layer of `.agents/` other than `rules/` is scaffolding, added as seams and actualized as the engine grows; each file carries its own status line, and a stub is never quoted as an authoritative rule.
- `style/naming.md` does **not** compile as one translation unit, by design: it re-declares its own sample entities (`E_DeviceState`, `var_g`, `IS_Drawable`) across fences, and the aggregate mode reports those as duplicate definitions. The green mode is one translation unit per fence.
- The ultimate example (§10 of `style/naming.md`) is the only fragment that must link and run, not merely compile: it carries `main`. `style/documentation.md` makes the opposite claim for its own fragments — they form a single translation unit — and that claim is verified by compiling them together.
- `style/naming.md` carries no frontmatter and no per-file scope metadata: nothing auto-attaches the rule documents to a path. The index in `AGENTS.md` is the only router, so a new artifact that is not linked there is invisible.

## Environment Quirks

- `g++` on PATH is a shim to GCC 12 (`/usr/bin/x86_64-linux-gnu-g++-12`), while the newest GCC is `g++-16` and Clang is 23. A verification report must name the compiler and its version — see [`../docs/toolchain.md`](../docs/toolchain.md).
- `doxygen` and `clang-format` are installed, but the repository has neither a `Doxyfile` nor a `.clang-format`: the documentation rules and the formatting rules are not enforced by any tool yet.
- No build system exists (no `CMakeLists.txt`, no `Makefile`; `cmake` and `ninja` are not installed), so `testing.md` and the build half of the pre-commit gate wait for a decision.

## Team Conventions

- Rules are edited in batches and committed only on an explicit request; a review of the batch (spelling, consistency, a gate run) comes first.
- Deviations, exemptions and placeholders are **findings** to report, never gaps to fill by assumption — see [`../policies/guardrails.md`](../policies/guardrails.md).
- A verification claim is quoted with the compiler, the version and the flag set actually used; an unverified claim is labelled as such instead of being softened.
