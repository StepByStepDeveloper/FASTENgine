# Working with agents

How this repository is developed with AI agents — and why nothing in it is required. The process itself is developer-first (ADR-0007): every stage is a command or a document a person carries alone, and an agent is an accelerator that plugs into the same stages. This chapter is the guide for when you use one.

**Status**: active — the rule behind it is ADR-0007; the directory map is [The repository](repository.md).

## The agent context

`.agents/` is a layer of optional accelerators — skills, commands, guardrails, personas, state. A person reads it as documentation; an agent loads it as behavior; nothing in the build, the gates or CI reads it at all ([The repository](repository.md) maps it entry by entry). The design file by file is the adapter table (`.agents/adapters/README.md`).

## The loop, with and without an agent

The same [process](process.md), two ways to drive it:

| Stage | By hand | With an agent |
|:--|:--|:--|
| Specify | Copy `docs/specs/_templates/spec.adoc` and write it ([guide](documentation/specs.md)) | Prompt `.agents/commands/new-spec.md`; skill `write-spec` — the agent drafts, you decide |
| Decide | `python3 tools/new_adr.py "Title"` ([guide](documentation/adr.md)) | Skill `write-adr` — it drafts the record; the owner accepts |
| Plan and slice | Copy the plan and tasks templates, fill them ([guide](documentation/specs.md)) | The same skills; the agent keeps identifiers and Bazel targets aligned |
| Agree | The architectural review and feature planning; the owner sets *Approved* | Helps prepare the review; never approves its own work |
| Implement | Red-green-refactor per the [walkthrough](process.md); `doit test` | Skill `tdd-cycle`, command `.agents/commands/implement-task.md` — one task, one test, one passing commit |
| Verify | `doit verify`, `doit trace`, `doit docs_check` | Command `.agents/commands/verify-rules.md`; expect raw command output, not a summary |
| Commit | Your commit message per [Git & PR workflow](conventions/git.md) | `.agents/commands/commit.md` drafts it; the commit happens when you ask |

## What you give an agent

- A task — one behavior from `tasks.adoc` — or a whole feature to plan. The agent context is already in the repository; you do not retype the manual into the prompt.
- The standing rules arrive by themselves: `AGENTS.md` is the entry point, and the guardrails under `.agents/policies/` bind the agent exactly as this manual binds you.
- When a harness does not read `AGENTS.md` natively, the adapters table explains how to port the tree.

## Guardrails that matter most

The full set is `.agents/policies/guardrails.md`; three rules shape every session:

- **Commits**: an agent never commits on its own initiative — commits happen when you ask. The secret scan blocks a commit that carries a finding.
- **Tests**: an agent never weakens a test, a rule or a gate to get green; that is a stop-and-ask.
- **Ambiguity**: when something is unclear, the agent stops and asks — the same rule that binds you.

The `ignore` list (`.agents/ignore`) names the paths an agent never reads.

## The agent's state

Two working notes live in `.agents/state/`: `scratchpad.md` — one task, written and reread while the agent works, cleared when it ends — and `memory.md` — durable facts about the project. They are working notes, not documentation: read them when you want to know what the agent believes, and correct them when they are wrong.

## When there is no agent

Nothing above is a dependency. Unplug the agent and the process is unchanged: every stage in the table has a by-hand column, and both columns run the same gates. If a rule ever seems to require an agent to execute it, that rule is wrong — fix it in [Process (SDD + ADR + TDD)](conventions/process.md), which is the binding description.

## A naming constraint

Agent harnesses gate writes to a few instruction-file basenames — `agents.md`, `claude.md`, `soul.md`, `.cursorrules` — wherever they appear, case-insensitively: every edit to a file with such a name requires an interactive approval. The root [`AGENTS.md`](../../AGENTS.md) is the one deliberate member of that set in this tree; everything else stays out of it, this chapter included — hence `working-with-agents.md`, not `agents.md`.

## Where to next

- [Documentation guides](documentation/README.md) — how the specifications, the decision records and the architecture document are written.
- [Conventions](conventions/README.md) — the binding rules behind the stages above.
- [Glossary](glossary.md) — every term this manual uses, in one place.
