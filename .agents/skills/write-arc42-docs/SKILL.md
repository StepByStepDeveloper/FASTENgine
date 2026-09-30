---
name: write-arc42-docs
description: "Write and maintain the arc42 architecture document — sections, diagrams, cross-references. Use whenever a change touches docs/arc42/** or the architecture narrative."
---

# Write the arc42 Documentation

How to edit FASTENgine's architecture document: which file owns what, how sections, diagrams and references stay consistent, and how to prove the result. The binding conventions live in [docs.md](../../../docs/development/conventions/docs.md); this skill is the procedure.

**Status**: active — the document is in template state; the procedure holds for both filling and maintaining it.

## When to Use

- A change alters the architecture narrative: a building block, a context, a runtime or deployment view.
- A diagram is added or changed (`docs/arc42/diagrams/*.puml`).
- A section's placeholder text is being replaced with content (§1–§12).
- Diagnosing why a section, an include or an anchor breaks `doit docs_check`.

## Procedure

1. **Pick the owning section file** in `docs/arc42/sections/` — one file per arc42 section, stable names and anchors (`[[section-*]]`). Never create a second file for the same section.
2. **Fill inside the structure.** Keep the heading levels; replace the `**<...>**` placeholders with content. Keep the `ifdef::arc42help[]` help while the document is a template — a filled section carries no placeholders of its own.
3. **Diagrams**: write `docs/arc42/diagrams/<name>.puml`, run `doit diagrams` to render `docs/arc42/images/<name>.svg`, and reference the render (`image::<name>.svg[alt text]`) — never the `.puml`. Renders are generated and never committed.
4. **Cross-references**: an ADR is included into Section 9, so link it internally as `<<adr-NNNN,ADR-NNNN>>`; for other files use `xref:path[text]`. A file-form xref does not become an internal link in the single-page build.
5. **Section 9 is generated territory.** Its index table and include list are written by `tools/new_adr.py` only — to add a decision, use the `write-adr` skill.
6. **Run the checks** — `python3 tools/check_docs.py` and `doit docs` — and keep the tree green before reporting.

## Quick Reference

```bash
doit diagrams      # .puml -> docs/arc42/images/*.svg
doit docs_check    # tree consistency: ADRs, regions, includes, links, images
doit docs          # full build into build/docs/
```

## Pitfalls

- The master `arc42.adoc` is the only file that attaches sections; a section file edited alone changes the built document only after `doit docs`.
- Markdown is not allowed under `docs/arc42/` — the AsciiDoc sources are the contract.
- `docs/arc42/images/*.svg` are generated: never commit or hand-edit them. `check_docs` accepts an image reference backed by a `.puml` source even before the first render.
- `:arc42help:` in `config.adoc` gates the help chrome for the whole document; removing it while placeholders remain is a rule violation.
- The Doxygen architecture pages (`build/docs/api-pages/`) are converted from these sections by `tools/render_arc42_pages.py` inside `doit docs`: edit the sources, never the converted pages.

## Verification

`doit docs_check` reports PASS, `doit docs` builds without asciidoctor warnings, and the edited section appears with its expected number in `build/docs/arc42/arc42.html` and, converted, among the Doxygen pages of `build/docs/api/html/`.
