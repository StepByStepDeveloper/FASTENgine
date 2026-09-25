# Hook: pre-commit gate

Automation **specification** — intent, not a harness config.

**Status**: stub — three of its four steps have no tooling behind them yet. The order below is the contract: a later step never runs on an artifact an earlier step already rejects.

```
on:     pre-commit
match:  any change under .agents/ or src/
action: the gate below, in order
mode:   blocking
```

1. **Context tree** — `.agents/skills/verify-rules/` exits 0 (rules compile, links and anchors resolve). *Available today.*
2. **Formatting** — `clang-format --dry-run --Werror` over the changed sources. *Waiting for `.clang-format`. *
3. **Build** — the project's build command. *Waiting for a build system (see [`../docs/toolchain.md`](../docs/toolchain.md)).*
4. **Tests** — the test command of the chosen framework (see [`../rules/testing.md`](../rules/testing.md)). *Waiting for the framework decision.*
