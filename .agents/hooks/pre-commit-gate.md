# Hook: pre-commit gate

Automation **specification** — intent, not a harness config.

**Status**: active — every step has its tooling today. `.githooks/pre-commit` runs the first step and the documentation check on its own; the rest run on request through `doit`. The order below is the contract: a later step never runs on an artifact an earlier step already rejects.

```
on:     pre-commit
match:  any change under AGENTS.md, .agents/, docs/ or src/
action: the gate below, in order
mode:   blocking
```

1. **Context tree** — `doit verify` exits 0 (conventions compile, links resolve, anchors and layout hold; the specifications validate). *Runs in `.githooks/pre-commit` and in CI.*
2. **Documentation** — `doit docs_check` exits 0 and `doit docs` builds (arc42, ADRs, API reference, Doxygen architecture pages — see [`docs/development/conventions/docs.md`](../../docs/development/conventions/docs.md)). *CI runs both in the Documentation job; `.githooks/pre-commit` runs the check for staged `docs/` or `tools/` changes (advisory).*
3. **Formatting** — `doit format_check` (`clang-format --dry-run --Werror` over the changed sources, per `.clang-format`). *Available today; nothing to check until `src/` carries sources.*
4. **Build** — `doit build` (Bazel, see [`../../docs/development/toolchain.md`](../../docs/development/toolchain.md)). *Available today; no targets until the first `BUILD.bazel`.*
5. **Tests** — `doit test` (GoogleTest / GoogleMock, see [`../../docs/development/conventions/testing.md`](../../docs/development/conventions/testing.md)). *Available today; no targets yet.*
