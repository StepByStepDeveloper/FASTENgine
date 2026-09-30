# FASTENgine

High-performance C++ engine. The repository today carries its specification layer: the agent context in `.agents/`, the architecture documentation in `docs/arc42/`, and `src/` waiting for the first modules.

## Start here

This page is the entry point. From here:

1. **[Development manual](docs/development/README.md)** — the walkthrough of working in this repository: layout, toolchain, workflows, documentation guides. Read it first.
2. **[Conventions](docs/development/conventions/README.md)** — the binding rules for code, tests, commits and documentation.
3. **[Architecture documentation](docs/arc42/arc42.adoc)** — the arc42 document of the engine (AsciiDoc; build it with `doit docs`).
4. **[The API site](docs/development/documentation/api.md)** — the Doxygen build, including the architecture as converted pages; publishable as a standalone site.
5. **[Agent context](AGENTS.md)** — for AI agents working in this repository.

## Working here in one minute

```bash
doit                      # the CI set: verify + build + test
doit verify               # specification gates (context tree + conventions)
doit build && doit test   # Bazel via Bazelisk
doit docs                 # build all documentation into build/docs/
```

Requirements — `doit`, Bazel 9 (via Bazelisk), `clang++` 23 or `g++-16`, and for the docs `asciidoctor`, `pandoc`, `plantuml`, `doxygen`. Versions, paths and the user-local installs: [Toolchain](docs/development/toolchain.md).

## How this repository keeps order

- **Three kinds of documentation, never mixed**: the [development manual](docs/development/README.md) (how to work here), the [product documentation](docs/arc42/arc42.adoc) (the engine itself) and the [agent context](AGENTS.md) (agent-only artifacts that link, not copy). The split is a recorded decision: [ADR-0002](docs/arc42/adr/0002-decompose-documentation-by-audience.adoc).
- **Gates run on every change**: the pre-commit hook scans for secrets and checks the trees; CI runs the same gates plus build, test and the docs build. A change is complete only when the documentation it invalidates changes with it.
- **Decisions are recorded**: anything with alternatives and lasting consequences becomes an [ADR](docs/development/documentation/adr.md) — tooling, structure, an expensive-to-change API.
- **Everything generated is a build artifact**: `build/**` and `docs/arc42/images/*.svg` are produced by `doit`, never committed.
