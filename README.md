# FASTENgine

FASTENgine - Fast Engine, be careful, fasten your seat belt.

A high-performance C++ engine. The repository currently carries the specification layer rather than engine code: the agent-facing context lives in `.agents/`, and `src/` holds the area skeletons only.

## Where the rules live

| Path | Holds |
|:--|:--|
| [`AGENTS.md`](AGENTS.md) | Entry point for coding agents: core rules, commands, the context router |
| [`.agents/rules/`](.agents/rules/style.md) | Binding conventions — style, testing, git |
| [`.agents/policies/guardrails.md`](.agents/policies/guardrails.md) | Prohibitions that outrank convenience |

## Toolchain

| Tool | Role |
|:--|:--|
| `clang++` 23, `g++-16` | C++17 front ends — see [`.agents/docs/toolchain.md`](.agents/docs/toolchain.md) |
| Bazel 9, through Bazelisk | Build — the version is pinned in `.bazelversion`, dependencies in `MODULE.bazel` |
| `doit` | Task runner — `dodo.py` |
| GoogleTest / GoogleMock | Tests |

## Run

```bash
doit verify   # context-tree gates: snippets compile, links, anchors and layout resolve
doit build    # bazel build //...
doit test     # bazel test //...
doit format   # clang-format over src/
```
