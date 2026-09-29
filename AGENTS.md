# FASTENgine

## Overview

High-performance C++ Engine. The repository currently carries the specification layer rather than engine code: the agent-facing context lives in `.agents/`, and `src/` waits empty — see [Toolchain](.agents/docs/toolchain.md) for what is installed and what is missing.

## Core Rules

- **Language**: All artifacts (code, documentation, comments, commit messages, etc.) must be created in English.
- **Ambiguity**: If any part of a task, requirement, or context is unclear, do not make assumptions. Ask the user for clarification instead.
- **Documentation**: Every piece of code created in this project must be accompanied by detailed Doxygen comments — see [Documentation (Doxygen)](.agents/rules/style/documentation.md) for the mandatory coverage, the required commands and the documented exceptions. The architecture, the decisions and the API reference are documented as code under `docs/` — see [Documentation system](.agents/rules/docs.md).
- **Guardrails**: Prohibitions that outrank convenience live in [Policies / Guardrails](.agents/policies/guardrails.md); the paths an agent must not read are listed in `.agents/ignore`.

## Commands

- **Verify the context tree**: `doit verify` — the three gates; the compile run alone is `python3 .agents/skills/verify-rules/scripts/verify_rule_docs.py .agents --group block --compiler clang++ --std c++17`
- **Build**: `doit build` — Bazel 9 through Bazelisk (`.bazelversion`, `MODULE.bazel`); the second front end is `bazel build //... --config=gcc16`
- **Test**: `doit test` — GoogleTest / GoogleMock targets
- **Lint**: `doit format` (writes) and `doit format_check` (checks) — `clang-format` with the repository's `.clang-format`
- **Docs**: `doit docs` (arc42 + ADR + API HTML into `build/docs/`), `doit docs_check` (the tree's consistency), `doit diagrams` (PlantUML renders) — AsciiDoc sources under `docs/`, conventions in [Documentation system](.agents/rules/docs.md)

## Context Architecture (`.agents/`)

This table is the router: nothing attaches a rule to a path automatically, so an artifact that is not linked here is invisible.

| Path | Holds |
|:--|:--|
| [`rules/`](.agents/rules/style.md) | Binding conventions — [style](.agents/rules/style.md), [testing](.agents/rules/testing.md), [git](.agents/rules/git.md), [docs](.agents/rules/docs.md) |
| [`policies/`](.agents/policies/guardrails.md) + [`ignore`](.agents/ignore) | Prohibitions, and the paths never to read |
| [`skills/`](.agents/skills/verify-rules/SKILL.md) | On-demand procedures — `verify-rules`, `write-arc42-docs`, `write-adr`, `build-api-docs` |
| [`docs/`](.agents/docs/toolchain.md) | Dense system facts — `toolchain.md` |
| [`commands/`](.agents/commands/verify-rules.md) | Ready prompts — `verify-rules`, `add-rule` |
| [`state/`](.agents/state/scratchpad.md) | `scratchpad.md` (one task), `memory.md` (durable) |
| [`hooks/`](.agents/hooks/pre-commit-gate.md) | Automation specs — the git hooks realize parts of them |
| [`agents/`](.agents/agents/naming-auditor.md) | Reviewer personas for delegation |
| [`evals/`](.agents/evals/naming-compliance.md) | Agent-test scenarios with mechanical criteria |
| [`adapters/`](.agents/adapters/README.md) | Mapping this tree onto another harness |
| `mcp.json` | MCP servers — placeholder, none configured |

Layers other than `rules/` are scaffolding; each file states its own status in its header.
