# Development manual

Everything a developer needs to work on FASTENgine: what the repository looks like, which tools it expects, how a change travels from a specification to merged code, and how its documentation is written and maintained. The repository [`README.md`](../../README.md) is the entry point; this manual is the walkthrough behind it — the chapters are ordered to be read in sequence.

**Status**: active. Restructured into the development manual with ADR-0002: it is the canonical home of the conventions and the toolchain facts; the agent context (`.agents/`) links here instead of copying. Extended with the process chapters — getting started, the development process, the specifications guide, the glossary — in the SDD + ADR + TDD adoption (ADR-0005).

## Reading order

1. [Getting started](getting-started.md) — from a fresh clone to a green check, and the first change you will make.
2. [The repository](repository.md) — the layout, the documentation classes, where everything lives and why.
3. [Toolchain](toolchain.md) — what is installed on the development machine, with versions and paths.
4. [Workflows](workflows.md) — the day-to-day commands, the gates and hooks, and how a change is committed.
5. [The development process](process.md) — the walkthrough of a feature: specification, decisions, plan, tasks, TDD, close.
6. [Documentation guides](documentation/README.md) — writing and maintaining the documentation:
   - [Specifications](documentation/specs.md) — the `docs/specs/` artifacts: spec, plan and task list;
   - [The arc42 document](documentation/arc42.md) — sections, diagrams, the template manual;
   - [Architecture decisions](documentation/adr.md) — the ADR workflow;
   - [The API site](documentation/api.md) — Doxygen, module groups, the converted architecture pages.
7. [Conventions](conventions/README.md) — the binding rules for code, tests, commits, documentation and the process.
8. [Glossary](glossary.md) — every term and abbreviation this manual uses, in one place.

## The gates at a glance

| Command | Checks |
|:--|:--|
| `doit verify` | Snippets compile, links resolve, anchors and layout hold — over `.agents` and `docs/development` together; the specifications (`docs/specs/`) validate |
| `doit spec_check` | The specifications alone: structure, identifiers, statuses, links |
| `doit docs_check` | The documentation tree: ADR set, generated regions, includes, images, links |
| `doit trace` | Traceability: acceptance criteria against tests — the report lands in `build/trace/` |
| `doit docs` | Builds everything into `build/docs/`: arc42, ADRs, the converted architecture pages, the API site |

The pre-commit hook and CI run the same gates; the details are in [Workflows](workflows.md).
