# FASTENgine

## Overview

High-performance C++ Engine. The repository carries its documentation and context, not engine code: the agent context lives in `.agents/`, `src/` waits empty, and the developer-facing documentation starts at the repository [`README.md`](README.md). Repository knowledge — workflows, toolchain facts, conventions — lives in the development manual: [`docs/development/`](docs/development/README.md).

## Core Rules

- **Language**: All artifacts (code, documentation, comments, commit messages, etc.) must be created in English.
- **Ambiguity**: If any part of a task, requirement, or context is unclear, do not make assumptions. Ask the user for clarification instead.
- **Documentation**: Every piece of code created in this project must be accompanied by detailed Doxygen comments — see [Documentation (Doxygen)](docs/development/conventions/style/documentation.md). The architecture, the decisions and the API reference are documented as code under `docs/` — see [Documentation system](docs/development/conventions/docs.md).
- **Conventions**: The binding conventions live in the development manual — [conventions index](docs/development/conventions/README.md); this tree links them and never restates them.
- **Process**: Features follow SDD + ADR + TDD — specification, ADRs, plan, tasks, test-first; the rules: [Process](docs/development/conventions/process.md).
- **Guardrails**: Prohibitions that outrank convenience live in [Policies / Guardrails](.agents/policies/guardrails.md); the paths an agent must not read are listed in `.agents/ignore`.

## Commands

- **Verify**: `doit verify` — the gates over `.agents`, `docs/development` and the specifications (`docs/specs/`); the compile sweep alone: `python3 .agents/skills/verify-rules/scripts/verify_rule_docs.py .agents docs/development --group block --compiler clang++ --std c++17`
- **Build**: `doit build` — Bazel 9 through Bazelisk (`.bazelversion`, `MODULE.bazel`); the second front end is `bazel build //... --config=gcc16`
- **Test**: `doit test` — GoogleTest / GoogleMock targets
- **Lint**: `doit format` (writes) and `doit format_check` (checks) — `clang-format` with the repository's `.clang-format`
- **Docs**: `doit docs` (arc42 + ADR + API site with architecture pages into `build/docs/`), `doit docs_check` (tree consistency), `doit diagrams` (PlantUML renders) — see [Documentation system](docs/development/conventions/docs.md)

## Context Architecture (`.agents/`)

This table is the router: nothing attaches a rule to a path automatically, so an artifact that is not linked here is invisible. Everything repository-facing lives in [`docs/development/`](docs/development/README.md) — this tree links there instead of copying.

| Path | Holds |
|:--|:--|
| [`skills/`](.agents/skills/verify-rules/SKILL.md) | On-demand procedures — `verify-rules`, `write-arc42-docs`, `write-adr`, `build-api-docs`, `write-spec`, `tdd-cycle` |
| [`policies/`](.agents/policies/guardrails.md) + [`ignore`](.agents/ignore) | Prohibitions, and the paths never to read |
| [`rules/`](.agents/rules/README.md) | Placeholder — standing agent-only rules; empty by design until one passes the admission test |
| [`commands/`](.agents/commands/verify-rules.md) | Ready prompts — `verify-rules`, `add-rule`, `commit`, `new-spec`, `implement-task` |
| [`state/`](.agents/state/scratchpad.md) | `scratchpad.md` (one task), `memory.md` (durable) |
| [`hooks/`](.agents/hooks/pre-commit-gate.md) | Automation specs — the git hooks realize parts of them |
| [`agents/`](.agents/agents/naming-auditor.md) | Reviewer personas for delegation |
| [`evals/`](.agents/evals/naming-compliance.md) | Agent-test scenarios with mechanical criteria |
| [`adapters/`](.agents/adapters/README.md) | Mapping this tree onto another harness |
| `mcp.json` | MCP servers — placeholder, none configured |

Layers are scaffolding; each file states its own status in its header.
