# Hook: verify the context tree after an edit

Automation **specification** — intent, not a harness config; an adapter turns it into the form of the harness in use.

**Status**: the action runs today (`.agents/skills/verify-rules/`), what is missing is the automatic trigger. Harness-agnostic realization: a git hook — `.githooks/pre-commit` plus `git config core.hooksPath .githooks` — which fires for the owner's commits too, not only for an agent's.

```
on:     file-edit
match:  .agents/**/*.md
action: python3 .agents/skills/verify-rules/scripts/verify_rule_docs.py .agents/rules --group block --compiler clang++ --std c++17
mode:   advisory
```

Flip to `blocking` once the git hook is installed and the tree has been green for a round.
