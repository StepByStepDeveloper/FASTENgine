# FASTENgine

High-performance C++ engine. The repository today carries its documentation and context, not engine code: the agent context in `.agents/`, the architecture documentation in `docs/arc42/`, the specifications under `docs/specs/`, and `src/` waiting for the first modules.

## Start here

This page is the entry point. From here:

1. **[Development manual](docs/development/README.md)** — the walkthrough of working in this repository: getting started, the feature process end to end, layout, toolchain, workflows, documentation guides, and the glossary. Read it first.
2. **[Conventions](docs/development/conventions/README.md)** — the binding rules for code, tests, commits and documentation.
3. **[Architecture documentation](docs/arc42/arc42.adoc)** — the arc42 document of the engine (AsciiDoc; build it with `doit docs`).
4. **[The API site](docs/development/documentation/api.md)** — the Doxygen build, including the architecture as converted pages; publishable as a standalone site.
5. **[Agent context](AGENTS.md)** — for AI agents working in this repository.

## Working here in one minute

```bash
doit                      # the CI set: verify + build + test
doit verify               # gates: context tree + specifications
doit build && doit test   # Bazel via Bazelisk
doit docs                 # build all documentation into build/docs/
```

Requirements — `doit`, Bazel 9 (via Bazelisk), `clang++` 23 or `g++-16`, and for the docs `asciidoctor`, `pandoc`, `plantuml`, `doxygen`. Versions, paths and the user-local installs: [Toolchain](docs/development/toolchain.md). The full command set: [Workflows](docs/development/workflows.md).

## How this repository keeps order

- **Documentation in four classes, never mixed**: the [specifications](docs/specs/README.adoc) (what is built, before it exists), the [development manual](docs/development/README.md) (how to work here), the [product documentation](docs/arc42/arc42.adoc) (the engine itself) and the [agent context](AGENTS.md) (agent-only artifacts that link, not copy). The split is a recorded decision: [ADR-0002](docs/arc42/adr/0002-decompose-documentation-by-audience.adoc).
- **Features follow a process**: SDD + ADR + TDD — a specification before code, decisions as ADRs, tasks implemented test-first; recorded in [ADR-0005](docs/arc42/adr/0005-adopt-sdd-adr-tdd-as-the-feature-development-process.adoc) and the [process conventions](docs/development/conventions/process.md).
- **Gates run on every change**: the pre-commit hook blocks on secrets and runs the tree checks (advisory); CI runs the same checks with blocking authority, plus build, test and the docs build. A change is complete only when the documentation it invalidates changes with it.
- **Decisions are recorded**: anything with alternatives and lasting consequences becomes an [ADR](docs/development/documentation/adr.md) — tooling, structure, an expensive-to-change API.
- **Everything generated is a build artifact**: `build/**` and `docs/arc42/images/*.svg` are produced by `doit`, never committed.
