# Development conventions

The binding conventions of this repository: how code, tests, commits, features and documentation are made here. They bind every author — the human developer and the agent alike — and where a machine can check them, they are checked (`doit verify`, `doit spec_check`, `doit docs_check`, the pre-commit hook and CI).

**Status**: active. The conventions moved here from the agent context by [ADR-0002](../../arc42/adr/0002-decompose-documentation-by-audience.adoc); the canonical home of a convention is the development manual, and the agent context links here instead of restating them.

| Document | Governs |
|:--|:--|
| [Code Style & Patterns](style.md) | C++ style: [naming](style/naming.md), [formatting](style/formatting.md), [documentation comments](style/documentation.md), [patterns](style/patterns.md) |
| [Testing](testing.md) | test structure, naming and coverage expectations |
| [Git & PR Workflow](git.md) | branches, commits, pull requests |
| [Documentation System](docs.md) | the documentation classes, arc42, ADRs, diagrams and Doxygen |
| [Process (SDD + ADR + TDD)](process.md) | the feature lifecycle: specification, decisions, plan, tasks, the red-green-refactor cycle and the gates |

How these documents are read and maintained — the workflows around them, the toolchain facts and the template manual — lives in the [development manual](../README.md).

**Where to next**: the [Glossary](../glossary.md) — every term these documents use, in one place; the [manual index](../README.md) is the way back to the reading order.
