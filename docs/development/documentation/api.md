# The API site

The Doxygen site is the standalone reference that can be published on a web resource: the API of the engine sources **and** the architecture document, converted from the arc42 AsciiDoc sources into Doxygen pages. The binding rules are the [Documentation System](../conventions/docs.md); the comment-level rules for C++ entities are [Documentation (Doxygen)](../conventions/style/documentation.md).

## What it contains

- The **API reference** — files, classes, functions — generated from `src/` with warnings as the coverage check (`EXTRACT_ALL = NO`, `WARN_IF_UNDOCUMENTED = YES`: an undocumented entity warns).
- The **modules** tree — the group map in `docs/api/groups.dox`, mirroring Section 5 of the arc42 document; a new building block joins the map and the section in the same change.
- The **architecture pages** — the twelve arc42 sections, converted from `docs/arc42/sections/` by `tools/render_arc42_pages.py` into `build/docs/api-pages/` and listed under *Related Pages*.

## Building

```bash
doit docs                                # everything, including the site
# or the API site alone, from the repository root:
mkdir -p build/docs/api && doxygen docs/api/Doxyfile
```

Open `build/docs/api/html/index.html`. Doxygen resolves the Doxyfile's relative paths against the directory it is started from — run it from the repository root only.

## The architecture pages pipeline

`tools/render_arc42_pages.py` (run by `doit docs`) converts each section: Asciidoctor (HTML5, help blocks off) → pandoc → Markdown, into `build/docs/api-pages/`, which the Doxyfile lists as INPUT. The conversion is deliberately best-effort: tables and lists survive, same-page anchors degrade to plain text, and links between sections stay page links. **The AsciiDoc sources stay the contract** — edit `docs/arc42/`, never the converted pages.

## Publishing

The site is self-contained under `build/docs/api/html/` — copy that directory to any static host. CI uploads `build/docs/` as an artifact; wiring GitHub Pages is not done yet.

## Pitfalls

- A warning is the coverage check working, not noise; quote unexpected warnings, do not silence them.
- `build/docs/api` is not created by doxygen itself — `mkdir -p` it, or let `doit docs` do it.
- `WARN_AS_ERROR` flips to `FAIL_ON_WARNINGS` together with the first stable engine sources — an open item in the [Documentation System](../conventions/docs.md).
- Anything under `build/` is a build artifact — a fix belongs in `docs/arc42/` (pages) or `docs/api/` (configuration).

## Verification

`doxygen docs/api/Doxyfile` exits 0 with no `warning:` lines; `build/docs/api/html/index.html` lists the module groups and its *Related Pages* tree carries the architecture overview and the twelve section pages.
