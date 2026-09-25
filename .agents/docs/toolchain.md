# Toolchain

What the rules assume and what is actually installed on this machine.

**Status**: active — measured on 2026-09-25. Re-measure before quoting a version inside a rule.

There is **no build system yet**: `cmake` and `ninja` are absent, and the repository has neither a `CMakeLists.txt` nor a `Makefile`. The commands below are therefore what a rule check runs against today.

## Compilers

| Tool | Version | Path | Notes |
|:--|:--|:--|:--|
| `clang++` | 23.1.2 | `/usr/local/bin/clang++` | target `x86_64-pc-linux-gnu`; the front end the warning claims of `style/naming.md` and `style/documentation.md` were measured on |
| `g++` | 12.4.0 | `/usr/bin/x86_64-linux-gnu-g++-12`, reached through a shim at `~/.local/bin/g++` | **not** the newest GCC here — a report that says "g++" must name which one it means |
| `g++-16` | 16.2.0 | `/usr/local/gcc-16.2.0` | the newest GCC on this machine |

## Other tools

| Tool | Version | Path | Notes |
|:--|:--|:--|:--|
| `doxygen` | 1.18.0 | `/usr/local/bin/doxygen` | no `Doxyfile` in the repository yet |
| `clang-format` | 23.1.2 | `/usr/local/bin/clang-format` | no `.clang-format` yet — the tool would fall back to LLVM style, which `style/formatting.md` does not describe |
| `clangd` | 23.1.2 | `/usr/local/bin/clangd` | language server |
| `make` | 4.3 (GNU) | `/usr/bin/make` | |

Absent: `cmake`, `ninja`, `gdb`, `ctest`.

## C++ standard

- Minimum: **C++17** — `style/patterns.md` prefers it, and every fragment of `style/naming.md` is written to compile as C++17; a C++20 form named in prose is an optional refinement of the same rule.
- Sweep targets for verification: `c++17`, `c++20`, `c++23`.

## Verification

Commands and their pitfalls live in the [`verify-rules` skill](../skills/verify-rules/SKILL.md); this document deliberately does not repeat them.

## Layout

| Path | What it will hold | State |
|:--|:--|:--|
| `src/algorithms/` | Algorithm implementations | empty (`.gitkeep`) |
| `src/patterns/` | Static-polymorphism implementations, per `style/patterns.md` | empty (`.gitkeep`) |
| `src/types/` | Core types | empty (`.gitkeep`) |
| `docs/` | Project documentation — the rules do not yet state what belongs here | empty (`.gitkeep`) |
| `.agents/` | Context architecture; the entry point is the repository `AGENTS.md` | active |
