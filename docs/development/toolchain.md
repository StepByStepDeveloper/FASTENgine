# Toolchain

What the conventions assume and what is actually installed on this machine.

**Status**: active — measured on 2026-09-28, extended on 2026-09-30 (the documentation toolchain); moved into the development manual with ADR-0002. Re-measure before quoting a version inside a rule.

The build is **Bazel 9**, installed through Bazelisk and pinned by `.bazelversion`; `doit` runs the tasks defined in `dodo.py`, and GoogleTest with GoogleMock arrives as a Bazel module dependency (`MODULE.bazel`). The distro's `cmake`, `ninja` and `vcpkg` are absent and are not used.

## Compilers

| Tool | Version | Path | Notes |
|:--|:--|:--|:--|
| `clang++` | 23.1.2 | `/usr/local/bin/clang++` | target `x86_64-pc-linux-gnu`; the front end the warning claims of `style/naming.md` and `style/documentation.md` were measured on; the default of `.bazelrc` (`--config=clang`) |
| `g++` | 12.4.0 | `/usr/bin/x86_64-linux-gnu-g++-12`, reached through a shim at `~/.local/bin/g++` | **not** the newest GCC here — a report that says "g++" must name which one it means |
| `g++-16` | 16.2.0 | `/usr/local/gcc-16.2.0` | the newest GCC on this machine; the second front end of `.bazelrc` (`--config=gcc16`) |
| `gcc` | 13.3.0 | `/usr/bin/gcc` | **no C++ front end**: `cc1plus` is not installed for gcc-13, so nothing may auto-detect the system compiler — Bazel names one explicitly |

## Other tools

| Tool | Version | Path | Notes |
|:--|:--|:--|:--|
| `bazel` | 9.2.0 | `~/.local/bin/bazel` (Bazelisk 1.29.0) | the version comes from `.bazelversion`; C++ rules and GoogleTest are module dependencies |
| `doit` | 0.37.0 | `~/.local/bin/doit` | the task runner — `dodo.py` |
| `doxygen` | 1.18.0 | `/usr/local/bin/doxygen` | `docs/api/Doxyfile`; `doxygen docs/api/Doxyfile`, run from the repository root, is the coverage check |
| `clang-format` | 23.1.2 | `/usr/local/bin/clang-format` | `.clang-format` in the repository root, reproducing the examples of `style/documentation.md` |
| `clangd` | 23.1.2 | `/usr/local/bin/clangd` | language server |
| `make` | 4.3 (GNU) | `/usr/bin/make` | |
| `asciidoctor` | Asciidoctor.js 2.2.9 (Asciidoctor 2.0.23), CLI 3.5.0 | `~/.local/bin/asciidoctor` (npm `@asciidoctor/cli@3.5.0`) | the HTML build of the AsciiDoc documentation (`doit docs`); the CLI is pinned at 3.5.0 — 4.0.0 is broken on Node 22; ships no docbook5 converter — the Doxygen-page pipeline is HTML5 + pandoc |
| `node` | 22.23.2 | `node` on PATH | the runtime of the Asciidoctor.js CLI |
| `pandoc` | 3.12 | `~/.local/bin/pandoc` (static release) | converts the arc42 sources into the Doxygen pages (`tools/render_arc42_pages.py`); CI installs it from apt |
| `plantuml` | 1.2026.8 | `~/.local/bin/plantuml` (wrapper) | the diagram pre-render (`doit diagrams`): runs `~/.local/share/plantuml/plantuml.jar` on a user-local Temurin 21 JRE (`~/.local/opt/temurin-21-jre`) because the system `java` is 8 — too old for current PlantUML releases |

Absent: `cmake`, `ninja`, `vcpkg`, `gdb`, `ctest` — the chosen stack does not need them; the Ruby toolchain (`asciidoctor-pdf`) is not installed either, so PDF output stays deferred ([Documentation system](conventions/docs.md)).

## C++ standard

- Minimum: **C++17** — `style/patterns.md` prefers it, and every fragment of `style/naming.md` is written to compile as C++17; a C++20 form named in prose is an optional refinement of the same rule. The build takes the standard from `.bazelrc` (`--cxxopt=-std=c++17`).
- Sweep targets for verification: `c++17`, `c++20`, `c++23`.

## Verification

Commands and their pitfalls live in the [`verify-rules` skill](../../.agents/skills/verify-rules/SKILL.md); this document deliberately does not repeat them.

## Layout

| Path | What it will hold | State |
|:--|:--|:--|
| `src/algorithms/` | Algorithm implementations | empty (`.gitkeep`) |
| `src/patterns/` | Static-polymorphism implementations, per `style/patterns.md` | empty (`.gitkeep`) |
| `src/types/` | Core types | empty (`.gitkeep`) |
| `docs/` | arc42 AsciiDoc sources, ADRs, diagram sources, the Doxygen input, the specifications under `docs/specs/` and the development manual under `docs/development/` — the system is [Documentation system](conventions/docs.md) | active |
| `MODULE.bazel`, `.bazelversion`, `.bazelrc` | Bazel workspace: module dependencies, the pinned version, the compiler and warning flags | active |
| `dodo.py` | doit tasks — the commands a developer and CI run | active |
| `tools/` | Tooling: the ADR generator, the documentation tree checker, the specification validator (`spec_check.py`), the traceability reporter (`trace.py`), the diagram renderer | active |
| `.clang-format`, `docs/api/Doxyfile` | The configuration the formatting and documentation rules are checked with | active |
| `.agents/` | Agent context architecture — agent-only artifacts, linking into the development manual; the entry point is the repository `AGENTS.md` | active |
