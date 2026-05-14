# Skill: agent-md-refactor

Refactor bloated agent instruction files (AGENTS.md, CLAUDE.md, etc.) to follow **progressive disclosure principles** - keeping essentials at root and organizing the rest into linked, categorized files.

## Triggers
Use this skill when:
- "refactor my AGENTS.md" / "refactor my CLAUDE.md"
- "split my agent instructions"
- "organize my CLAUDE.md file"
- "my AGENTS.md is too long"

## Process

### Phase 1: Find Contradictions
Identify any instructions that conflict with each other (e.g., contradictory style guidelines). Ask the user to resolve before proceeding.

### Phase 2: Identify the Essentials
Extract ONLY what belongs in the root agent file. The root should be minimal - information that applies to **every single task**.
- Project description (one sentence)
- Package manager
- Non-standard commands
- Critical overrides
- Universal rules

### Phase 3: Group the Rest
Organize remaining instructions into logical categories (e.g., `typescript.md`, `testing.md`, `code-style.md`, `architecture.md`).

### Phase 4: Create the File Structure
Output a structure like:
```
project-root/
├── AGENTS.md (Minimal root with links)
└── .kilo/
    └── agent/
        ├── typescript.md
        ├── testing.md
        └── ...
```

### Phase 5: Flag for Deletion
Identify and remove redundant, vague, or outdated instructions.

## Verification
1. Root file is minimal (under 50 lines).
2. All links work correctly.
3. No contradictions remain.
