# Hook: verify the context tree after an edit

Automation **specification** — intent, not a harness config; an adapter turns it into the form of the harness in use.

**Status**: active — the trigger is realized as a git hook: `.githooks/pre-commit` runs the whole gate (compile, links, anchors, layout) for any commit touching `AGENTS.md` or `.agents/`, the owner's commits included. Enable it once per clone with `git config core.hooksPath .githooks`; CI runs the same gate (`.github/workflows/context-tree.yml`).

```
on:     file-edit
match:  AGENTS.md and .agents/**/*.md
action: python3 .agents/skills/verify-rules/scripts/verify_rule_docs.py .agents --group block --compiler clang++ --std c++17
mode:   advisory
```

Flip to `blocking` once the tree has been green for a round — the hook prints a problem and lets the commit through today.
