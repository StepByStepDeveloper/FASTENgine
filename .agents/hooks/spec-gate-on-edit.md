# Hook: validate the specifications after an edit

Automation **specification** — intent, not a harness config; an adapter turns it into the form of the harness in use.

**Status**: active — the trigger is realized as a git hook: `.githooks/pre-commit` runs the check for any staged change under `docs/specs/` (advisory until the gate has been green for a round); CI runs the same check (`.github/workflows/context-tree.yml`).

```
on:     file-edit
match:  docs/specs/**/*.adoc
action: python3 tools/spec_check.py docs/specs
mode:   advisory
```

Traceability (`doit trace`) is the companion check — it needs sources, so it runs in CI and on demand rather than per edit. Flip to `blocking` together with its sibling [verify-rules-on-edit.md](verify-rules-on-edit.md).
