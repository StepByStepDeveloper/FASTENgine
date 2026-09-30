# SCRATCHPAD — active task

Operational memory of **one** task: the agent writes and rereads it while working, and clears it when the task ends. This is a working note, not a report — keep it short.

**Status**: complete — the `rules/` placeholder is in place, routed, and gated; every gate is green, awaiting the owner's review (committing is a separate request).

## Objective

Give the residual category of agent-only rules a declared home: a documented `rules/` placeholder with an admission test, a layout gate that admits it, and the routing updated — without reopening the decomposition's decisions.

## Status

- [x] `.agents/rules/README.md` — placeholder + admission test + neighbour table
- [x] layout check: placeholder-only admission for `rules/` (fails on any other member) and the router route required
- [x] `add-rule` routes a norm by type first; memory + verify-rules skill note updated
- [x] ADR-0004 created, filled, index regenerated; `doit docs` / `docs_check` green
- [x] skill `agent-rules-docs`: admission-test criterion + `verify_rule_docs.py` upstreamed (multi-root; four vendored copies byte-identical again)
- [x] `AGENTS.md` router row for `rules/` — added with the owner's approval; the row is now checked mechanically
- [x] gates: layout green, `doit verify` PASS, `doit docs_check` PASS, `doit docs` rc=0

## Discovered Issues

- The vendored `verify_rule_docs.py` had drifted from the skill copy (the repo carried the newer multi-root version) — upstreamed into the skill; byte-identity restored and checked with `diff -rq`.
- `AGENTS.md` is gate-protected: a write needs the owner's approval — expect a confirmation prompt when editing it.
- A placeholder that exists but is not routed is invisible — the layout check now fails when the `AGENTS.md` row is missing.

## Next action

None — the owner reviews the diff; committing happens on an explicit request.
