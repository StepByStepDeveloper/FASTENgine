---
name: verify-rules
description: "Verify the specification tree — snippets compile, links and anchors resolve. Use before any commit that touches .agents/ or docs/development/."
---

# Verify the Specification Tree

Mechanical gate for the specification tree — the agent context and the development conventions: every fenced C++ block is compiled, every relative link is resolved, every numbered heading and in-page anchor is checked. The conventions are binding text, and a fragment that does not compile teaches the wrong thing silently — so a change under `.agents/` or `docs/development/` is verified by running code, not by reading it twice.

**Status**: active scaffold — which fenced languages are compiled by the script is a choice of the script, not of this document.

## When to Use

- Before committing any change under `.agents/` or `docs/development/` (conventions, manual, policies, skills, commands).
- After editing a fenced example, a heading, an anchor or a cross-reference anywhere in the two trees.
- When the owner asks whether the specification tree is still green.

## Scripts

All five live in `scripts/` (Python 3, standard library only). Four of them are copies of the agent-side skill `agent-rules-docs`: pull updates from that skill instead of editing the copies, so the two do not drift apart. The fifth is authored here.

| Script | What it checks |
|:--|:--|
| `verify_rule_docs.py <dir> [<dir> ...]` | Compiles every fenced block of a compilable language and resolves every relative markdown link, across one or more roots (`.agents`, `docs/development`). `--group block` is one translation unit per fence. |
| `check_heading_numbering.py <doc>` | A hand-numbered document: dot depth against heading level, sequential siblings, every `#anchor` resolved against the regenerated slugs. |
| `check_context_layout.py [--root .agents]` | The context tree against its reference layout: the entries, the per-layer structure (frontmatter, sections, hook fields, the `AGENTS.md` shape), that the conventions live under `docs/development/conventions/`, and that `rules/` stays a placeholder until a rule passes its admission test. |
| `audit_examples.py <doc>` | One document in depth: per-fence compile bare and with prelude on every compiler, fenced-line length census, comment column alignment, whole-document translation unit, token sweep. |
| `probe_fence.py <doc>` | Dumps one fence (the largest by default) as a standalone file — for a build / link / run check. |

## How to Run

The standard the rules promise is **C++17**, so pass it explicitly — the script's own default is `c++20`:

```bash
# one translation unit per fence: the mode that is green for naming.md
python3 .agents/skills/verify-rules/scripts/verify_rule_docs.py .agents docs/development \
    --group block --compiler clang++ --std c++17

# the numbered document
python3 .agents/skills/verify-rules/scripts/check_heading_numbering.py \
    docs/development/conventions/style/naming.md -r docs/development/conventions
```

Full sweep — three front ends × three standards:

```bash
for c in clang++ g++ g++-16; do for std in c++17 c++20 c++23; do
  python3 .agents/skills/verify-rules/scripts/verify_rule_docs.py docs/development/conventions \
      --group block --compiler "$c" --std "$std" >/dev/null || echo "FAIL $c $std"
done; done
```

Links across the whole specification tree, not only the conventions subtree:

```bash
python3 .agents/skills/verify-rules/scripts/verify_rule_docs.py .agents docs/development --group block
```

The three runs above are wrapped as `doit verify` (`dodo.py`) — the entry point `.githooks/pre-commit` and `.github/workflows/context-tree.yml` call.

Layout conformance of the tree itself — run it after adding, renaming or removing a layer:

```bash
python3 .agents/skills/verify-rules/scripts/check_context_layout.py --root .agents --repo .
```

## Pitfalls

- **`--group tree` and `--group file` are the wrong mode for `naming.md`.** That document re-declares its own sample entities (`E_DeviceState`, `var_g`, `IS_Drawable`) in several fences, so an aggregate build reports duplicate definitions — that is the mode, not a snippet defect. `--group block` is the green mode, and the document makes no single-translation-unit claim.
- **Name the compiler.** `g++` on this machine's PATH is a shim to GCC 12 while the newest GCC is `g++-16`; a report that says "g++" without a version is verified on something else — see [`../../../docs/development/toolchain.md`](../../../docs/development/toolchain.md).
- **Warnings are expected.** The fragments declare names nothing reads, so `-Wall -Wextra -Wpedantic` reports unused-declaration warnings. Exit 0 with warnings is a pass: quote the warnings in the report, never call the run clean.
- **"Not compiled" is not a pass.** With no compiler on PATH the script writes the unit to a temp file and reports it unverified; count such a line as a gap, not as green.
- **A doc claiming a single translation unit needs its own run.** `style/documentation.md` makes that claim for its own fragments; it is checked by compiling them together, not by the per-fence mode alone.

## Verification

Passing means: `verify_rule_docs.py` exits 0 for every compiler × standard pair, `check_heading_numbering.py` exits 0 for every numbered document, every relative link resolves, and any warning you did not expect is quoted in the report.
