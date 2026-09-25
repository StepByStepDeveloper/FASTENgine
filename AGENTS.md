# FASTENgine

## Overview

High-performance C++ Engine. The repository currently carries the specification layer rather than engine code: the agent-facing context lives in `.agents/`, and `src/` waits empty — see [Toolchain](.agents/docs/toolchain.md) for what is installed and what is missing.

## Core Rules

- **Language**: All artifacts (code, documentation, comments, commit messages, etc.) must be created in English.
- **Ambiguity**: If any part of a task, requirement, or context is unclear, do not make assumptions. Ask the user for clarification instead.
- **Documentation**: Every piece of code created in this project must be accompanied by detailed Doxygen comments — see [Documentation (Doxygen)](.agents/rules/style/documentation.md) for the mandatory coverage, the required commands and the documented exceptions.
- **Guardrails**: Prohibitions that outrank convenience live in [Policies / Guardrails](.agents/policies/guardrails.md); the paths an agent must not read are listed in `.agents/ignore`.

## Commands

- **Verify the context tree**: `python3 .agents/skills/verify-rules/scripts/verify_rule_docs.py .agents/rules --group block --compiler clang++ --std c++17`
- **Build**: `[Insert Build Command, e.g., cmake --build build]` — pending, no build system yet (see [Toolchain](.agents/docs/toolchain.md))
- **Test**: `[Insert Test Command, e.g., ctest --test-dir build]` — pending
- **Lint**: `[Insert Lint Command, e.g., clang-format -i src/*.cpp]` — pending, no `.clang-format` yet

## Context Architecture (`.agents/`)

This table is the router: nothing attaches a rule to a path automatically, so an artifact that is not linked here is invisible.

| Path | Holds |
|:--|:--|
| [`rules/`](.agents/rules/style.md) | Binding conventions — style, testing, git |
| [`policies/`](.agents/policies/guardrails.md) + [`ignore`](.agents/ignore) | Prohibitions, and the paths never to read |
| [`skills/`](.agents/skills/verify-rules/SKILL.md) | On-demand procedures — `verify-rules` |
| [`docs/`](.agents/docs/toolchain.md) | Dense system facts — `toolchain.md` |
| [`commands/`](.agents/commands/verify-rules.md) | Ready prompts — `verify-rules`, `add-rule` |
| [`state/`](.agents/state/scratchpad.md) | `scratchpad.md` (one task), `memory.md` (durable) |
| [`hooks/`](.agents/hooks/pre-commit-gate.md) | Automation specs — none realized yet |
| [`agents/`](.agents/agents/naming-auditor.md) | Reviewer personas for delegation |
| [`evals/`](.agents/evals/naming-compliance.md) | Agent-test scenarios with mechanical criteria |
| [`adapters/`](.agents/adapters/README.md) | Mapping this tree onto another harness |
| `mcp.json` | MCP servers — placeholder, none configured |

Layers other than `rules/` are scaffolding; each file states its own status in its header.
