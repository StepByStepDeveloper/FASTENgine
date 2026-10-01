# Getting started

You have the repository in front of you and want to build something. This chapter takes you from a fresh clone to a green check in one sitting. The full tour of how changes are made here is [The development process](process.md) — read it once before your first feature; this chapter is the twenty minutes before that.

## 1. What you need

The toolchain this repository expects is measured, versioned and listed in [Toolchain](toolchain.md): Bazel (through Bazelisk), `doit`, a C++ compiler — `clang++` is the default — and, for documentation builds, Asciidoctor.js, pandoc and PlantUML. Install what that document lists; everything below assumes the same tool names on `PATH`. No `cmake`, no `ninja`, no `vcpkg` — the stack deliberately does not use them.

## 2. First commands

```bash
git clone <url> FASTENgine
cd FASTENgine
git config core.hooksPath .githooks   # once per clone: enables the pre-commit gate
```

Then look around without changing anything:

```bash
doit list        # every task this repository defines
doit verify      # the gates: fenced snippets compile, links resolve, layout holds
```

`doit verify` is green on a fresh clone, and it is the command you will run most. The build and test tasks know the repository's current state — `src/` is empty today, so they report that state instead of failing:

```bash
doit build       # bazel build //... — nothing to build until the first BUILD file
doit test        # bazel test //...  — nothing to run until the first BUILD file
```

The full documentation build needs the documentation tools on `PATH`; it produces the arc42 site and the API reference under `build/docs/` (never committed):

```bash
doit docs
```

## 3. The map

| Where | What lives there |
|:--|:--|
| `src/` | the engine — empty until the first modules; you will add the first `BUILD.bazel` yourself |
| `docs/specs/` | what is being built and how it will be verified — the process artifacts |
| `docs/arc42/` | the architecture document and the ADRs |
| `docs/api/` | the Doxygen configuration and the module group map |
| `docs/development/` | this manual |
| `.agents/` | the agent context — skills, policies, hooks, evals |
| `tools/`, `dodo.py` | the tooling and the task runner |

One level deeper — the three documentation classes, and why the split is binding — is [The repository](repository.md).

## 4. The first change you will make

There are two kinds of changes, and they differ in what “done” means:

- **A fix or a small helper**: a failing test first, then the fix — one commit, one PR. No specification, no ADR.
- **A feature**: it starts with a specification, not with code. In short: write `docs/specs/NNN-<slug>/spec.adoc` from the templates, get it *Approved*, record the decisions that need an ADR, write the plan and the tasks, then implement task by task in the red-green-refactor loop. The step-by-step walkthrough, with a worked example, is [The development process](process.md).

Two rules apply to both kinds, and they are the ones newcomers trip over:

- **A red gate stops the change.** Fix the artifact, never the gate — no weakened tests, no silenced warnings, no `--no-verify`.
- **Documentation changes in the same commit.** Code changes are incomplete until the documentation they invalidate is updated with them — the checklists that decide what “the documentation” means are in [Process](conventions/process.md).

## 5. Where the rules live

The binding conventions are indexed in [Conventions](conventions/README.md): code style, naming, tests, commits, the documentation system and the process itself. They cite each other; when two documents seem to disagree, follow the one that owns the topic, and fix the other.

Curious about a term this manual keeps using? [Glossary](glossary.md) has them all in one place.

## Where to next

- [The repository](repository.md) — the full map of the layout.
- [Workflows](workflows.md) — the day-to-day commands and the automatic gates.
- [The development process](process.md) — the walkthrough of a feature, start to finish.
