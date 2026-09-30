# Adapters

The rest of `.agents/` is canonical — alongside the development conventions under `docs/development/conventions/` — and harnesses do not look there by themselves: each one reads its own paths (`.cursor/rules/`, `.claude/settings.json`, `.mcp.json`, …). This file maps the canonical artifacts onto those paths. A symlink is preferred — it leaves one source of truth; a generator is the fallback where symlinks are unavailable.

**Status**: stub — one row is active (the native one); the rest are the steps to take when a second harness is used. Nothing here is generated today.

| Harness | Expects | Source | Method |
|:--|:--|:--|:--|
| Hermes, Codex CLI, Cursor, Claude Code (fallback) | `AGENTS.md` (repository root) | — | none — it is the open standard and is already in place |
| Hermes project skills | `<repo-root>/.agents/skills/` | `.agents/skills/` | read in place, but the repository must be trusted once: `hermes skills trust` (recorded in `skills.trusted_project_dirs`) |
| Cursor / Windsurf | `.cursor/rules/*.mdc`, `.windsurf/rules/*.md` | `docs/development/conventions/**/*.md` | symlink — *would need* the `description` / `globs` / `alwaysApply` frontmatter the conventions documents do not carry today |
| Cursor | `.cursorignore` | `.agents/ignore` | symlink |
| Claude Code | `.mcp.json` | `.agents/mcp.json` | symlink |
| Claude Code | `.claude/settings.json` (hooks) | `.agents/hooks/*.md` | generate — the specs are intent-level and need translation |
| Claude Code | `.claude/skills/<name>/`, `.claude/agents/<name>.md` | `.agents/skills/`, `.agents/agents/` | symlink |

## Notes

- Hermes delivers a subdirectory `AGENTS.md` automatically when a session touches files in that directory (32 KiB ceiling; keep an area file well under it), so per-area guidance needs no adapter — it needs the file.
- A harness not listed above reads nothing from `.agents/` and needs a new row here first.
- Project skills are the highest-precedence tier for Hermes sessions started inside this repository, and the curator never modifies them — but they also do not load until the repository is trusted.
