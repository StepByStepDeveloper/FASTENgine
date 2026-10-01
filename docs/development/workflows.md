# Workflows

The day-to-day: which command to run, what the gates check, and how a change travels from edit to commit.

## The task runner

Everything runs through [doit](https://pydoit.org) (`dodo.py`); a developer and CI execute the same tasks.

| Command | What it does |
|:--|:--|
| `doit` | The CI set: `verify` + `build` + `test` |
| `doit verify` | The specification gates: snippets compile, links resolve, anchors and layout hold; the specifications (`docs/specs/`) validate |
| `doit spec_check` | The specifications alone: structure, identifiers, statuses, links |
| `doit build` / `doit test` | Bazel build / test of `//...` — currently a state report, until the first `BUILD.bazel` |
| `doit format` / `doit format_check` | `clang-format` over `src/` — writes / checks without writing |
| `doit docs` | Builds all documentation into `build/docs/` |
| `doit docs_check` | Checks the documentation tree alone |
| `doit trace` | The traceability report — acceptance criteria against tests, into `build/trace/` |
| `doit diagrams` | Renders `docs/arc42/diagrams/*.puml` into `docs/arc42/images/*.svg` |

## Editing and the gates

- **Code**: match the [conventions](conventions/README.md) — naming, formatting, Doxygen comments; run `doit format` and then `doit verify` before reporting.
- **Documentation**: after editing under `docs/`, run `doit docs_check` and `doit docs` — see the [documentation guides](documentation/README.md).
- **Specification text** (`.agents/`, `docs/development/`): run `doit verify`; fenced blocks of compilable languages are compiled with `clang++`, and links across both trees are resolved.
- **Specifications** (`docs/specs/`): run `doit spec_check` after every edit; statuses move only per the [process conventions](conventions/process.md), and the criteria-against-tests side is `doit trace`.

The gates also run automatically:

| Where | What runs | Blocking? |
|:--|:--|:--|
| `.githooks/pre-commit` | secret scan, any staged change | yes — a finding blocks the commit |
| `.githooks/pre-commit` | specification gate (for `.agents/`, `docs/development/`, `docs/specs/` or `AGENTS.md` changes) | advisory today |
| `.githooks/pre-commit` | documentation tree check (for `docs/` or `tools/` changes) | advisory today |
| CI *Context tree* job | the same specification gate, plus `doit trace` | yes |
| CI *Build and test* job | `doit build`, `doit test` | yes |
| CI *Documentation* job | `doit docs_check`, `doit docs` | yes |

Enable the hooks once per clone: `git config core.hooksPath .githooks`.

## Committing

Branch, commit and PR conventions live in [Git & PR Workflow](conventions/git.md): Conventional Commits in the imperative mood, one theme per change, verification evidence quoted in the message or the PR. A change is complete only when the documentation it invalidates is updated in the same commit — see the [Documentation System](conventions/docs.md).

## Bazel in one minute

The build is Bazel 9 through Bazelisk; the version is pinned in `.bazelversion`. `doit build` runs `bazel build //...` with the default `--config=clang`; the second front end is `bazel build //... --config=gcc16`. GoogleTest arrives as a Bazel module dependency (`MODULE.bazel`). Details and versions: [Toolchain](toolchain.md).

## Local documentation builds

`doit docs` needs `asciidoctor`, `pandoc`, `plantuml` and `doxygen` on `PATH` — install notes in the [toolchain facts](toolchain.md). The output lands in `build/docs/`: the architecture document at `build/docs/arc42/arc42.html`, the standalone API site at `build/docs/api/html/index.html`. Nothing under `build/` is ever committed.
