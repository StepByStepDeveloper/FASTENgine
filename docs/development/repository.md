# The repository

What lives where, and why. One sentence per design goal: the product documentation describes the product, the development manual describes how the repository is worked on, and the agent context carries only what an agent reads.

## Top level

| Path | Holds |
|:--|:--|
| `src/` | The engine sources — `algorithms/`, `patterns/`, `types/`; empty until the first modules and their `BUILD.bazel` |
| `docs/arc42/` | The arc42 architecture document (AsciiDoc), the ADR set, the diagram sources |
| `docs/api/` | The Doxygen configuration, the main page and the module group map |
| `docs/development/` | This manual — workflows, toolchain facts, documentation guides, the conventions, the arc42 template copy |
| `.agents/` | The agent context — skills, policies, hooks, evals, state; no developer prose, only links out |
| `tools/` | Documentation tooling: the ADR generator, the tree checker, the diagram renderer, the pages converter |
| `MODULE.bazel`, `.bazelrc`, `.bazelversion` | The Bazel workspace: dependencies, the pinned version, compiler and warning flags |
| `dodo.py` | The task runner — one command set for a developer and CI |
| `.githooks/` | The pre-commit gate: a blocking secret scan plus advisory tree checks |
| `.github/workflows/` | CI: the specification gate, build/test, the documentation job |

## Three kinds of documentation

| Class | Home | Read by | Carries |
|:--|:--|:--|:--|
| Agent context | `AGENTS.md`, `.agents/` | the agent | only artifacts an agent reads; links out for everything repository-facing |
| Development manual | `README.md`, `docs/development/` | anyone working on the repository | how to work here: workflows, toolchain, conventions, templates |
| Product documentation | `docs/arc42/`, `docs/api/` (built into `build/docs/`) | readers of the product | architecture, decisions, API reference, the converted architecture pages |

The split is binding ([ADR-0002](../arc42/adr/0002-decompose-documentation-by-audience.adoc)): a fact lives in exactly one class, and the other classes link to it. When unsure where a new document belongs, ask *who reads it* — an agent, a contributor, or a consumer of the engine.

## Where to go next

- How the repository is worked on: [Workflows](workflows.md).
- The toolchain facts: [Toolchain](toolchain.md).
- The documentation system in detail: [Documentation guides](documentation/README.md).
- The binding rules: [Conventions](conventions/README.md).
