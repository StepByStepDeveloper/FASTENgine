# Development manual

Everything a developer needs to work on FASTENgine: what the repository looks like, which tools it expects, how the everyday workflows run, and how its documentation is written and maintained. The repository [`README.md`](../../README.md) is the entry point; this manual is the walkthrough behind it.

**Status**: active. Restructured into the development manual with ADR-0002: it is the canonical home of the conventions and the toolchain facts; the agent context (`.agents/`) links here instead of copying.

## Reading order

1. [The repository](repository.md) — the layout, the three documentation classes, where everything lives and why.
2. [Toolchain](toolchain.md) — what is installed on the development machine, with versions and paths.
3. [Workflows](workflows.md) — the day-to-day commands, the gates and hooks, and how a change is committed.
4. [Documentation guides](documentation/README.md) — writing and maintaining the documentation:
   - [The arc42 document](documentation/arc42.md) — sections, diagrams, the template manual;
   - [Architecture decisions](documentation/adr.md) — the ADR workflow;
   - [The API site](documentation/api.md) — Doxygen, module groups, the converted architecture pages.
5. [Conventions](conventions/README.md) — the binding rules for code, tests, commits and documentation.

## The gates at a glance

| Command | Checks |
|:--|:--|
| `doit verify` | Snippets compile, links resolve, anchors and layout hold — over `.agents` and `docs/development` together |
| `doit docs_check` | The documentation tree: ADR set, generated regions, includes, images, links |
| `doit docs` | Builds everything into `build/docs/`: arc42, ADRs, the converted architecture pages, the API site |

The pre-commit hook and CI run the same gates; the details are in [Workflows](workflows.md).
