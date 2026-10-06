# Documentation guides

How the documentation of this repository is written and maintained. The binding rules are the [Documentation System](../conventions/docs.md) — these pages are the working guides around it, and where they disagree, the convention wins.

## The sources of truth

| Source | Format | Built by | Guide |
|:--|:--|:--|:--|
| Specifications | AsciiDoc (`docs/specs/`) | — (plain sources; gated by `doit spec_check`) | [Specifications](specs.md) |
| Architecture document | AsciiDoc (`docs/arc42/`) | `doit docs` | [The arc42 document](arc42.md) |
| Decisions | AsciiDoc ADRs (`docs/arc42/adr/`) | `doit docs` | [Architecture decisions](adr.md) |
| API reference and architecture pages | Doxygen (`docs/api/`, `src/`) | `doit docs` | [The API site](api.md) |

## The build in one look

```bash
doit spec_check    # the specifications (docs/specs)
doit trace         # acceptance criteria ↔ tests (build/trace/)
doit diagrams      # .puml -> .svg
doit docs_check    # tree consistency (ADRs, regions, includes, links, images)
doit docs          # everything -> build/docs/ (arc42, ADRs, pages, API site)
```

`build/docs/arc42/arc42.html` is the rendered architecture document; `build/docs/api/html/index.html` is the standalone Doxygen site — the API reference plus the architecture as converted pages. Generated output is never committed.

## The template manual

The repository keeps the upstream arc42 template as the manual of *what each section must contain*: [arc42-template/](arc42-template/README.md) — the official English AsciiDoc sources, vendored under CC BY-SA 4.0. Read it when filling a section for the first time.

## Where to next

- [Conventions](../conventions/README.md) — the binding rules these guides orbit; the [Documentation System](../conventions/docs.md) is the one that owns them.
- [Glossary](../glossary.md) — the terms, gathered in one place.
