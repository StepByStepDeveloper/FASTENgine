# Hook: pre-commit gate

Automation **specification** — intent, not a harness config.

**Status**: active — every step has its tooling today. `.githooks/pre-commit` runs the first step on its own; the other three run on request through `doit`. The order below is the contract: a later step never runs on an artifact an earlier step already rejects.

```
on:     pre-commit
match:  any change under AGENTS.md, .agents/ or src/
action: the gate below, in order
mode:   blocking
```

1. **Context tree** — `doit verify` exits 0 (rules compile, links, anchors and layout resolve). *Runs in `.githooks/pre-commit` and in CI.*
2. **Formatting** — `doit format_check` (`clang-format --dry-run --Werror` over the changed sources, per `.clang-format`). *Available today; nothing to check until `src/` carries sources.*
3. **Build** — `doit build` (Bazel, see [`../docs/toolchain.md`](../docs/toolchain.md)). *Available today; no targets until the first `BUILD.bazel`.*
4. **Tests** — `doit test` (GoogleTest / GoogleMock, see [`../rules/testing.md`](../rules/testing.md)). *Available today; no targets yet.*
