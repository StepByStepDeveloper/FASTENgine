# Hook: secret scan on commit

Automation **specification** — intent, not a harness config; an adapter turns it into the form of the harness in use.

**Status**: active — realized as `.githooks/check_secrets.py`, run by `.githooks/pre-commit` for any staged change, the owner's commits included. Unlike the context-tree gate it is blocking from day one: a finding stops the commit. Enable the hook once per clone with `git config core.hooksPath .githooks`.

```
on:     pre-commit
match:  any staged change, in any path
action: python3 .githooks/check_secrets.py — reads the staged (index) content and the staged file names, prints `<path>:<line>: <rule>` findings, exits 1 on a finding
mode:   blocking
```

The policy it enforces is the first prohibition of [`../policies/guardrails.md`](../policies/guardrails.md): no credential ever enters a file of this repository. The scan is heuristic — it recognizes shapes, reads the index rather than the working tree, skips binary content, and exempts a line that carries an `allowlist-secret` marker with a reason. It does not scan history or CI runs; GitHub's own secret scanning and push protection remain the server-side complement for commits made without the hook.
