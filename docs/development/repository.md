# The repository

Where everything lives, why it is there, and what to touch when. The classes of documentation — specifications, the manual, product documentation, the agent context — are defined in [Documentation system](conventions/docs.md); this chapter is their map, one level deeper.

```
fastengine/
├── .agents/                 the agent context — optional accelerators, read by agents alone
│   ├── adapters/            how this tree maps onto another agent harness
│   ├── agents/              reviewer personas for delegation
│   ├── commands/            ready-made prompts for the manual's procedures
│   ├── evals/               scenarios the agent context is tested against
│   ├── hooks/               automation specs (the git hooks realize parts of them)
│   ├── policies/            guardrails, and the ignore list — what an agent must not do or read
│   ├── rules/               (placeholder) standing agent-only rules
│   ├── skills/              on-demand procedures — verify-rules, write-spec, write-adr, write-arc42-docs, build-api-docs, tdd-cycle
│   └── state/               scratchpad.md (one task, local) and memory.md (durable facts)
├── .github/                 CI and the pull-request checklist
│   └── workflows/           one workflow, three jobs: the context-tree gate, the build, the documentation build
├── .githooks/               the git hooks: the secret scan first, the advisory tree checks after
├── docs/
│   ├── api/                 the Doxygen configuration and the site pages
│   ├── arc42/               product documentation — the architecture, the decisions, the diagrams
│   │   ├── adr/             the decision records: the template and ADR-0001 onward
│   │   ├── diagrams/        PlantUML sources
│   │   ├── images/          rendered diagrams (generated, not committed)
│   │   └── sections/        the twelve arc42 sections
│   ├── development/         the development manual — start at its README
│   └── specs/               the specifications: _templates/ and NNN-<slug>/ per feature
├── src/                     the implementation — algorithms/, patterns/, types/
├── tools/                   repository scripts: new_adr.py, spec_check.py, check_docs.py, trace.py, the renderers
├── AGENTS.md                the entry point for AI agents — the project rules and where the context lives
├── dodo.py                  the doit task definitions: the commands a developer and CI run
├── MODULE.bazel             the Bazel module: the dependencies — rules_cc, GoogleTest
├── .bazelversion            the pinned Bazel version
└── .bazelrc                 the build configurations: clang (default) and gcc16
```

## The source tree

The layout of `src/` is fixed; adding a directory is a decision, not a convenience:

| Path | What it holds |
|:--|:--|
| `src/algorithms/` | Algorithm implementations. |
| `src/patterns/` | Static-polymorphism implementations, per [Build patterns](conventions/style/patterns.md). |
| `src/types/` | Core types. |

Every directory will carry a `BUILD.bazel` naming it a Bazel package; the target and test naming comes from [Build patterns](conventions/style/patterns.md). The directories sit empty (`.gitkeep`) until the first feature lands.

## The agent context (`.agents/`)

The one directory that is not the project proper: a layer of optional accelerators for working with AI agents. Nothing in the build or the tests reads it; the gates only check that it stays consistent — and every stage of the process runs by hand (ADR-0007). How to use it is [Working with agents](working-with-agents.md); its design, file by file, is the adapter table (`.agents/adapters/README.md`).

| Directory | Purpose |
|:--|:--|
| `skills/` | On-demand procedures — one `SKILL.md` per procedure, with the scripts and templates it needs; loaded when the task matches. |
| `commands/` | Ready-made prompts for the manual's procedures: `new-spec`, `implement-task`, `verify-rules`, `add-rule`, `commit`. |
| `policies/` | The guardrails — commit discipline, test integrity, ambiguity handling — and the `ignore` list of paths an agent never reads. |
| `rules/` | (placeholder) Standing agent-only rules; empty by design until one passes the admission test (ADR-0004). |
| `hooks/` | The automation specs; the git hooks implement parts of them. |
| `agents/` | Reviewer personas for delegation: naming, tests, documentation, rule-documentation. |
| `evals/` | Scenarios with mechanical criteria — they test the agent context itself. |
| `state/` | Two working notes: `scratchpad.md` (one task, cleared when it ends — local, git-ignored) and `memory.md` (durable facts about the project, committed). |
| `adapters/` | The mapping of this tree onto another agent harness — what to port, what to drop. |
| `mcp.json` | MCP server registrations; none configured yet. |

## Where to next

- [Toolchain](toolchain.md) — what is installed on this machine, with versions and paths.
- [Workflows](workflows.md) — the day-to-day commands and the automatic gates.
- [Conventions](conventions/README.md) — the binding rules behind the layout.
