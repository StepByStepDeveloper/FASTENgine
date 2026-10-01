# Documentation System (arc42, ADR, AsciiDoc, Doxygen)

FASTENgine documents its architecture, its decisions and its API reference as code: plain-text sources live in `docs/` and `README.md`, change in the same commits as the artifacts they describe, and pass mechanical checks. This rule binds the documentation system as a whole — the classes of documentation, the layout, the formats, the specifications, the decision records, the diagram pipeline and the Doxygen wiring. The comment-level rules for C++ entities are a separate document: [Documentation (Doxygen)](style/documentation.md).

**Status**: active — the layout, the tools and the checks exist; the twelve arc42 sections are handed to their authors in template state (arc42's own help texts on); the specifications (`docs/specs/`) carry the process artifacts (empty until the pilot).

## Documentation classes

Every document belongs to exactly one class; the classes cite each other, they never restate each other:

| Class | Home | Carries | Reader |
|:--|:--|:--|:--|
| Agent context | `AGENTS.md`, `.agents/` | only artifacts an agent reads: skills, policies, hooks, evals, state, the adapters map — and pointers, not copies, for everything repository-facing | the agent |
| Development manual | `README.md`, `docs/development/` | how to work in this repository: workflows, toolchain facts, the conventions, the documentation guides, the arc42 template manual | any developer joining the repository |
| Product documentation | `docs/arc42/`, `docs/api/` (built into `build/docs/`) | the product itself: architecture, decisions, API reference, the converted architecture pages | readers of the product |
| Specifications | `docs/specs/` | what is being built and how it will be verified, before it exists: requirements, acceptance criteria, the plan, the task list | the author and the reviewer of a feature |

The split is binding: the agent context does not carry developer prose it can link (it points into `docs/development/`), and the product documentation does not describe the repository's own process. Specifications state intent, arc42 states the architecture as built — they cross-reference, they never restate each other.

## Documentation as code

- **Single sources, not copies.** Every statement lives in exactly one artifact: the architecture narrative in the arc42 document, a decision's rationale in its ADR, the API contract in Doxygen comments, the conventions in this document set. Cross-link between them; never restate.
- **Same commit.** A change is incomplete until the documentation it invalidates is updated in the same commit — see *Definition of done* below.
- **Language**: English (the `Language` core rule of `AGENTS.md`).
- **Generated artifacts are never committed.** `build/docs/**` is produced by `doit docs`; the renders in `docs/arc42/images/*.svg` are produced by `doit diagrams`. Both are ignored by git: edit the source, rebuild, never touch the artifact.

## Layout

| Path | Holds | State |
|:--|:--|:--|
| `docs/arc42/arc42.adoc` | The master document — the only file that attaches the twelve sections | active |
| `docs/arc42/config.adoc` | Shared AsciiDoc attributes (`:toc:`, `:imagesdir:`, `:arc42help:`) | active |
| `docs/arc42/about-arc42.adoc` | Provenance block: template version, template license, adaptation note | active |
| `docs/arc42/sections/01…12_*.adoc` | One file per arc42 section; names and anchors are stable | template state (help texts on) |
| `docs/arc42/adr/adr-template.adoc` | The ADR template — the shape `tools/new_adr.py` fills | active |
| `docs/arc42/adr/NNNN-*.adoc` | One file per architecture decision record | active (ADR-0001 accepted) |
| `docs/arc42/diagrams/*.puml` | PlantUML diagram sources — the only editable form of a diagram | scaffold |
| `docs/arc42/images/` | Diagram renders (`*.svg`, generated) and committed static images | active |
| `docs/api/Doxyfile`, `docs/api/mainpage.md`, `docs/api/groups.dox` | Doxygen configuration, main page and the module group map | active |
| `docs/specs/` | The specifications: one directory per feature (`NNN-<slug>/` with `spec.adoc`, `plan.adoc`, `tasks.adoc`), the `_templates/` they start from, and the directory README | active (empty until the pilot) |
| `docs/development/` | The development manual: workflows, toolchain facts, documentation guides, the conventions and the arc42 template copy — indexed from the repository `README.md` | active |
| `tools/new_adr.py`, `tools/check_docs.py`, `tools/spec_check.py`, `tools/trace.py`, `tools/render_diagrams.py`, `tools/render_arc42_pages.py` | The documentation and specification tooling the commands below call | active |
| `build/docs/` | Built HTML (arc42, ADRs, API reference) and the converted Doxygen pages (`build/docs/api-pages/`) — generated, never committed | generated |

## Formats

- **AsciiDoc everywhere under `docs/`; no Markdown in `docs/arc42/`.** One text toolchain keeps includes, cross-references and tables uniform. The single exception is `docs/api/mainpage.md`, which Doxygen consumes directly.
- **Sections are edited, not composed ad hoc.** The master includes them in order; an include line is never duplicated; a section file is only built as part of the master, except in the mechanical Doxygen-page conversion (`tools/render_arc42_pages.py`).
- **Diagrams are sources first.** No image enters a section without a `.puml` (or an entry in `images/` that no tool regenerates) behind it — see *Diagrams*.

## The arc42 document

### Sections

- The twelve files in `docs/arc42/sections/` keep their names and their `[[section-*]]` anchors; nothing renumbers them, and the master lists them in arc42 order.
- Fill a section by replacing its placeholders inside the existing heading structure. Placeholders (`**<...>**`) and arc42 help chrome belong to template state only; a filled section carries neither.
- The help texts are gated by `:arc42help:` in `config.adoc` (defined = shown). When the document stops being a template: remove that line, update `:revremark:` in the master, and delete the dead help blocks section by section.
- Section 5 names the building blocks; `docs/api/groups.dox` mirrors that list — see *API reference*.

### Diagrams

- Sources: `docs/arc42/diagrams/<name>.puml` (PlantUML), rendered by `doit diagrams` into `docs/arc42/images/<name>.svg`.
- A section references the render as `image::<name>.svg[alt]` — never the `.puml`, never an absolute path.
- Rendering is a pre-render step, not an AsciiDoc extension: `asciidoctor-diagram` is deliberately absent (see *Toolchain state*).
- Static images no tool regenerates (screenshots, scans) may be committed under `images/`; they must not shadow a diagram render's name.

### ADRs and Section 9

- Every decision with alternatives and lasting consequences gets an ADR; one decision per file.
- Create only through the generator: `python3 tools/new_adr.py "Title"` — it numbers the file, fills the template and rewrites both generated regions of Section 9. Never create, rename or renumber an ADR file by hand.
- The number is the file name's first four digits, zero-padded; the anchor is `[[adr-NNNN]]`; the title line is `= ADR-NNNN: <Title>`. The generator, `tools/check_docs.py` and the Section 9 index read exactly these.
- The status line — directly under the title — has the fixed form `Status: <status> (<YYYY-MM-DD>).`, with `<status>` one of `proposed`, `accepted`, `rejected`, `deprecated`, `superseded by ADR-NNNN`. Only the line changes as the decision moves; the record below it does not.
- **An accepted ADR's substance is immutable.** Typos may be fixed; a decision that changes is *superseded*: write a new ADR and flip the old record's status line to `superseded by ADR-NNNN`.
- The two regions between the marker comments in `sections/09_architecture_decisions.adoc` are generated — never edit them by hand. `doit docs_check` fails when they drift from the files on disk; `python3 tools/new_adr.py --regenerate` rewrites them.
- Code that realizes a decision names it in its documentation block (`@note`, plain text `ADR-NNNN`); the ADR's *More Information* links back to the affected blocks and files.

## API reference (Doxygen)

- The configuration is `docs/api/Doxyfile`; the build runs **from the repository root** — paths inside resolve against the current directory.
- `docs/api/groups.dox` is the only place the module tree is listed. Every level-1 or level-2 building block named in Section 5 exists as a group there, and its members join the group from their own documentation blocks; a block is added to both lists in the same change.
- Coverage policy: `EXTRACT_ALL = NO` with `WARN_IF_UNDOCUMENTED = YES` — a warning is the coverage check working, not noise. `WARN_AS_ERROR` flips to `FAIL_ON_WARNINGS` together with the first stable engine sources (open item below).
- The standalone site also carries the architecture document as Doxygen pages: `tools/render_arc42_pages.py` converts the arc42 sections to Markdown under `build/docs/api-pages/` (Asciidoctor HTML5 -> pandoc; the conversion is deliberately best-effort — tables survive, exact anchors do not), and the Doxyfile lists that directory as INPUT. The AsciiDoc sources stay the contract; the converted pages are build artifacts.
- What must be documented, and how: [Documentation (Doxygen)](style/documentation.md).

## Commands

| Command | What it does |
|:--|:--|
| `doit docs` | Builds everything into `build/docs/`: renders diagrams, checks the tree, builds arc42 and the ADRs, converts the architecture pages, builds the API site |
| `doit docs_check` | Checks the tree alone: the ADR set and numbering, the generated regions, includes, image and link targets |
| `doit spec_check` | Validates the specifications (`docs/specs/`) — structure, identifiers, status, links (also one of the `doit verify` gates) |
| `doit trace` | Writes the traceability report (criteria against tests) into `build/trace/` |
| `doit diagrams` | Renders `diagrams/*.puml` to `images/*.svg`; skips up-to-date renders, `--force` re-renders |
| `python3 tools/new_adr.py "Title"` | Creates an ADR and regenerates the Section 9 regions; `--regenerate` rewrites the regions alone |
| `python3 tools/render_arc42_pages.py` | Converts `docs/arc42/sections/` into the Doxygen pages under `build/docs/api-pages/` (run by `doit docs`) |
| `doxygen docs/api/Doxyfile` | The API reference alone, from the repository root (`mkdir -p build/docs/api` first) |

CI runs `doit docs_check` and `doit docs` in the workflow job *Documentation*; the pre-commit hook adds the tree check for staged `docs/` or `tools/` changes (advisory).

## Definition of done (documentation half)

| Change | Documentation action in the same commit |
|:--|:--|
| New or changed level-1/2 building block | Section 5 entry + its group in `docs/api/groups.dox` + Doxygen blocks per [Documentation (Doxygen)](style/documentation.md) |
| A decision taken (alternatives, consequences) | A new ADR through the generator; supersede the old record when the decision replaces one |
| New or changed public entity | Doxygen comment block per [Documentation (Doxygen)](style/documentation.md) |
| A diagram changes | Edit the `.puml` source; `doit diagrams`; commit the source only |
| The architecture narrative changes | The owning section file; update the ADR references it carries |
| A feature is specified, replanned or advanced | The specifications (`docs/specs/NNN-<slug>/`): statuses and criteria per [Process](process.md) |
| A convention changes | The document under `docs/development/conventions/` that owns it; the artifact that stated it before changes in the same commit |

## Toolchain state

The toolchain is Asciidoctor.js (npm `@asciidoctor/cli`), pandoc and a user-local PlantUML on Temurin 21 — versions and paths measured in [`../toolchain.md`](../toolchain.md).

- The CLI is pinned to `@asciidoctor/cli@3.5.0`: 4.0.0 is broken on Node 22. CI installs the same pin — local and CI builds must not drift.
- The Doxygen-page conversion runs Asciidoctor with the HTML5 backend, not DocBook: Asciidoctor.js ships no docbook5 converter (measured), so the pipeline is HTML5 -> pandoc and the conversion is explicitly best-effort.
- PDF output and inline `asciidoctor-diagram` rendering are **deferred** with the Ruby toolchain: diagrams are pre-rendered by `doit diagrams`, and PDF returns when a build target for it exists.
- Doxygen's `WARN_AS_ERROR` is the same kind of open item — see *API reference*.

## Prohibited

- Hand-editing the generated regions of Section 9, the `build/docs/` tree, or `docs/arc42/images/*.svg`.
- Editing an accepted ADR's Context, Drivers, Options, Outcome or Consequences — supersede it with a new record.
- Renaming or renumbering a section file or an ADR file by hand; creating an ADR without the generator.
- A statement duplicated across arc42, an ADR and a Doxygen block instead of cross-linked.
- Requirement text copied between `docs/specs/`, the arc42 sections and the Doxygen blocks instead of referencing identifiers (`FR-NNN-ii`, `AC-NNN-ii`).
- Markdown under `docs/arc42/` — the AsciiDoc sources are the contract.
- Placeholder text left in a section declared filled, or `:arc42help:` removed while placeholders remain.
- Referencing an image that neither exists in `images/` nor has a `.puml` source behind it.

## Maintenance and verification

- The mechanical half of this rule is `tools/check_docs.py` — run it (or `doit docs_check`) after any change under `docs/` and quote its output in reports. The vendored arc42 template copy under `docs/development/documentation/arc42-template/` is excluded from its include/image/link scans by design (frozen third-party material, reported as a note).
- The snippets and links of this document set are verified by `doit verify`, together with the context tree it is linked from; a report names both gates when both are relevant.
