# Hook: check and rebuild the documentation after an edit

Automation **specification** — intent, not a harness config; an adapter turns it into the form of the harness in use.

**Status**: scaffold — the commands it names exist today (`python3 tools/check_docs.py`, `doit docs`); `.githooks/pre-commit` runs the check alone for staged `docs/` or `tools/` changes, and CI runs both in the *Documentation* job.

```
on:     file-edit
match:  docs/**, tools/check_docs.py, tools/render_diagrams.py, tools/new_adr.py, tools/render_arc42_pages.py
action: python3 tools/check_docs.py && doit docs
mode:   advisory
```

Flip to `blocking` once the documentation tree has been green for a round — the hook reports a problem and lets the commit through today.
