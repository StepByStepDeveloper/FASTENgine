# FASTENgine

High-performance C++ engine. The repository today carries its documentation and context, not engine code: the agent context in `.agents/`, the architecture documentation in `docs/arc42/`, the specifications under `docs/specs/`, and `src/` waiting for the first modules.

## Start here

This page is the entry point. From here:

1. **[Development manual](docs/development/README.md)** — the walkthrough of working in this repository: getting started, the feature process end to end, layout, toolchain, workflows, working with agents, documentation guides, and the glossary. Read it first.
2. **[Conventions](docs/development/conventions/README.md)** — the binding rules for code, tests, commits and documentation.
3. **[Architecture documentation](docs/arc42/arc42.adoc)** — the arc42 document of the engine (AsciiDoc; build it with `doit docs`).
4. **[The API site](docs/development/documentation/api.md)** — the Doxygen build, including the architecture as converted pages; publishable as a standalone site.
5. **[Agent context](AGENTS.md)** — the optional accelerator layer for AI agents; the human-facing guide to it is [Working with agents](docs/development/working-with-agents.md).

## Working here in one minute

```bash
doit                      # the CI set: verify + build + test
doit verify               # gates: context tree + specifications
doit build && doit test   # Bazel via Bazelisk
doit docs                 # build all documentation into build/docs/
```

Requirements — `doit`, Bazel 9 (via Bazelisk), `clang++` 23 or `g++-16`, and for the docs `asciidoctor`, `pandoc`, `plantuml`, `doxygen`. Versions and paths: [Toolchain](docs/development/toolchain.md). The full command set: [Workflows](docs/development/workflows.md).

## How this repository keeps order

- **Documentation in four classes, never mixed**: the [specifications](docs/specs/README.adoc) (what is built, before it exists), the [development manual](docs/development/README.md) (how to work here), the [product documentation](docs/arc42/arc42.adoc) (the engine itself) and the [agent context](AGENTS.md) (agent-only artifacts that link, not copy). The split is a recorded decision: [ADR-0002](docs/arc42/adr/0002-decompose-documentation-by-audience.adoc).
- **Features follow a process**: SDD + ADR + TDD — planning packages (specification, ADRs, plan, tasks) agreed at architectural review and feature planning, implementation later and test-first; recorded in [ADR-0005](docs/arc42/adr/0005-adopt-sdd-adr-tdd-as-the-feature-development-process.adoc), extended by [ADR-0006](docs/arc42/adr/0006-separate-architectural-planning-from-implementation-in-the-feature-process.adoc) (planning and implementation as two phases) and [ADR-0007](docs/arc42/adr/0007-keep-the-process-developer-first-with-agents-optional.adoc) (developer-first, agents optional); the rules: [process conventions](docs/development/conventions/process.md).
- **Gates run on every change**: the pre-commit hook blocks on secrets and runs the tree checks (advisory); CI runs the same checks with blocking authority, plus build, test and the docs build. A change is complete only when the documentation it invalidates changes with it.
- **Decisions are recorded**: anything with alternatives and lasting consequences becomes an [ADR](docs/development/documentation/adr.md) — tooling, structure, an expensive-to-change API.
- **Everything generated is a build artifact**: `build/**` and `docs/arc42/images/*.svg` are produced by `doit`, never committed.
