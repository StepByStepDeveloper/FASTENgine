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

### Compiler roles

`clang++` is the **reference front end**: the warning claims of the conventions were measured on it, the formatting and language services (`clang-format`, `clangd`) belong to it, and both gate runs — `doit verify` and CI — compile with it. Its build is **warning-free with `-Werror`** (`.bazelrc`, `--config=clang`): a warning anywhere in the engine fails the build. The one deliberate exception is the illustrative fragments of `docs/development/conventions/**` — they declare entities nothing reads by design, so the tree's gate compiles them without `-Werror`; the exemption itself is stated in `style/documentation.md`.

`g++-16` is the **portability front end**: it exists so that code touching a compiler's unspecified details (undefined behavior, floating-point contraction) is caught here rather than in a consumer's build, and Linux consumers build with GCC. Its contract is weaker on purpose — the code must compile and every test must pass under it, but `-Werror` is off there: the warning sets of the two compilers are not held equal, and a warning only GCC emits stays a warning.

### Selecting the front end

The two front ends are registered as Bazel configs in `.bazelrc` — `clang` and `gcc16` — and **the caller picks one; there is no rc-level default**. `doit build` and `doit test` pass `--config=clang`; the portability path is an explicit `bazel build //... --config=gcc16`. A bare `bazel build` with no flag falls back to Bazel's compiler autodetection (the PATH `cc`), which on this machine picks the C-less system `gcc` and fails by definition. The rc keeps no default because an `rc`-level `--config` expands for every command and the flags of stacked configs only accumulate — a default there would drag `-Werror` into the `gcc16` build. Two boards exist for local deviations: a git-ignored user rc (`user.bazelrc` and variants) for a developer's own overrides, and the tracked `.platform.bazelrc` for a platform fact that genuinely belongs to the repository; neither is in use today.

Measured as of 2026-10-10: the full sweep of the `verify-rules` skill is green on all three front ends (clang++ 23.1.2, g++ 12.4.0 through the shim, g++-16 16.2.0 — hence on both GCC versions this machine carries) × C++17/20/23.

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

The repository map — every directory with its purpose, including the agent-context tree — lives in [The repository](repository.md).

## Where to next

- [Workflows](workflows.md) — the day-to-day commands these tools run.
- [The development process](process.md) — where a change travels, start to finish.
- [Conventions](conventions/README.md) — the rules that assume this toolchain.
