#!/usr/bin/env python3
"""Render the arc42 sources into Doxygen user pages (Markdown).

The documentation is two things at once: the arc42 document of the product and
the source of the architecture chapter of the API site. This script converts
every section of ``docs/arc42/sections/`` into one Markdown page under
``build/docs/api-pages/``; ``docs/api/Doxyfile`` lists that directory as
INPUT, so ``doit docs`` assembles the standalone site in one run.

Pipeline, per section: Asciidoctor (HTML5, embedded) -> pandoc -> GitHub
flavoured Markdown. Two measured facts shape it: Asciidoctor.js has no
docbook5 converter (the backend aborts), and the arc42 help blocks disappear
with ``-a arc42help!``. A Lua filter unwraps the structural ``<div>``
wrappers; a post-pass promotes headings, numbers the page title, rewrites
image paths to the pages directory and turns ``#anchor`` links into sibling
page links where the anchor map knows the target.

The conversion is deliberately best-effort: tables, notes and lists survive;
exact in-page anchors do not — the AsciiDoc sources stay the contract. The
output is a build artifact under ``build/``; it is never committed.

Usage:
    python3 tools/render_arc42_pages.py [--root docs] [--out build/docs/api-pages]

Exit codes: 0 = every section converted; 1 = a conversion failed; 2 =
'asciidoctor' or 'pandoc' is missing from PATH, or the arc42 tree does not
exist.

Standard library only.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SECTION_STEMS = [
    "01_introduction_and_goals",
    "02_architecture_constraints",
    "03_context_and_scope",
    "04_solution_strategy",
    "05_building_block_view",
    "06_runtime_view",
    "07_deployment_view",
    "08_concepts",
    "09_architecture_decisions",
    "10_quality_requirements",
    "11_technical_risks",
    "12_glossary",
]

# Unwrap the structural <div> wrappers so the converted Markdown stays flat.
LUA_FILTER = """\
function Div(el)
  return el.content
end
"""

ANCHOR_RE = re.compile(r"^\[\[([A-Za-z0-9_-]+)\]\][ \t]*$", re.M)
SECTION_TITLE_RE = re.compile(r"^== (.+)$", re.M)
RAW_DIV_RE = re.compile(r"^\s*</?div[^>]*>\s*$", re.M)
HEADING_RE = re.compile(r"^#{2,6} ")
ANCHOR_LINK_RE = re.compile(r"\[([^\]]*)\]\(#([A-Za-z0-9_-]+)\)")
ADOC_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+\.adoc[^)]*)\)")


def build_anchor_map(root: Path) -> dict[str, str]:
    """Map every ``[[anchor]]`` reachable from the pages to its page file name."""
    mapping: dict[str, str] = {}
    for stem in SECTION_STEMS:
        path = root / "arc42" / "sections" / f"{stem}.adoc"
        if not path.is_file():
            continue
        for anchor in ANCHOR_RE.findall(path.read_text(encoding="utf-8")):
            mapping.setdefault(anchor, f"{stem}.md")
    # The ADR files are included by Section 9, so their anchors sit on that page.
    adr_dir = root / "arc42" / "adr"
    if adr_dir.is_dir():
        for adr in sorted(adr_dir.glob("[0-9]*.adoc")):
            for anchor in ANCHOR_RE.findall(adr.read_text(encoding="utf-8")):
                mapping.setdefault(anchor, "09_architecture_decisions.md")
    return mapping


def convert(asciidoctor: str, pandoc: str, lua: Path, section: Path, tmp_md: Path) -> bool:
    """Convert one section file to Markdown in ``tmp_md``; False on tool failure."""
    html = tmp_md.with_suffix(".html")
    proc = subprocess.run(
        [asciidoctor, "-b", "html5", "-s", "-a", "toc!", "-a", "arc42help!",
         "-o", str(html), str(section)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0 or "asciidoctor: ERROR" in (proc.stdout + proc.stderr):
        print(f"render_arc42_pages: asciidoctor FAILED: {section}")
        print(proc.stdout + proc.stderr)
        return False
    proc = subprocess.run(
        [pandoc, "-f", "html", "-t", "gfm", "--wrap=none",
         "--lua-filter", str(lua), str(html), "-o", str(tmp_md)],
        capture_output=True, text=True,
    )
    if proc.returncode != 0:
        print(f"render_arc42_pages: pandoc FAILED: {section}")
        print(proc.stdout + proc.stderr)
        return False
    return True


def postprocess(md: str, page: str, anchor_map: dict[str, str]) -> str:
    """Shape pandoc's Markdown into a Doxygen page (see the module docstring)."""
    md = RAW_DIV_RE.sub("", md)
    md = md.replace("](../images/", "](images/")

    def fix_anchor(match: re.Match[str]) -> str:
        text, anchor = match.group(1), match.group(2)
        target = anchor_map.get(anchor)
        if target and target != page:
            return f"[{text}]({target})"
        # Same-page and unknown anchors have no Doxygen target: keep the text.
        return text

    md = ANCHOR_LINK_RE.sub(fix_anchor, md)
    # Leftover AsciiDoc links: keep the visible text, drop the dead path.
    md = ADOC_LINK_RE.sub(r"\1", md)

    lines: list[str] = []
    in_fence = False
    title_pending = True
    for line in md.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and HEADING_RE.match(line):
            line = line[1:]
            if title_pending and line.startswith("# "):
                line = f"# {page[:2]}. " + line[2:]
                title_pending = False
        lines.append(line)

    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)) + "\n"


def overview_page(root: Path) -> str:
    """The index page of the generated architecture chapter."""
    lines = [
        "# Architecture (arc42)",
        "",
        "*This chapter is generated from the arc42 sources in `docs/arc42/` by",
        "`tools/render_arc42_pages.py` (run by `doit docs`). Edit the AsciiDoc",
        "sources, never this copy; the conversion is best-effort, so tables and",
        "cross-references may render plainer here than in the HTML build.*",
        "",
        "## Sections",
        "",
    ]
    for stem in SECTION_STEMS:
        source = root / "arc42" / "sections" / f"{stem}.adoc"
        if not source.is_file():
            continue
        title = SECTION_TITLE_RE.search(source.read_text(encoding="utf-8"))
        name = title.group(1).strip() if title else stem
        lines.append(f"- [{stem[:2]}. {name}]({stem}.md)")
    lines += [
        "",
        "Decisions: the ADR set lives in `docs/arc42/adr/` and is included by",
        "Section 9 of the document.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", default="docs", help="the documentation root (default: docs)")
    parser.add_argument("--out", default="build/docs/api-pages",
                        help="the pages directory (default: build/docs/api-pages)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    sections_dir = root / "arc42" / "sections"
    if not sections_dir.is_dir():
        print(f"render_arc42_pages: arc42 tree not found under {root}")
        return 2

    asciidoctor = shutil.which("asciidoctor")
    pandoc = shutil.which("pandoc")
    if asciidoctor is None or pandoc is None:
        print("render_arc42_pages: need 'asciidoctor' and 'pandoc' on PATH — "
              "see docs/development/toolchain.md")
        return 2

    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    anchor_map = build_anchor_map(root)
    sections = [stem for stem in SECTION_STEMS if (sections_dir / f"{stem}.adoc").is_file()]

    failed = 0
    with tempfile.TemporaryDirectory() as tmp_name:
        tmp = Path(tmp_name)
        lua = tmp / "unwrap.lua"
        lua.write_text(LUA_FILTER, encoding="utf-8")
        for stem in sections:
            source = sections_dir / f"{stem}.adoc"
            tmp_md = tmp / f"{stem}.md"
            if not convert(asciidoctor, pandoc, lua, source, tmp_md):
                failed += 1
                continue
            page = out / f"{stem}.md"
            page.write_text(
                postprocess(tmp_md.read_text(encoding="utf-8"), page.name, anchor_map),
                encoding="utf-8",
            )
            print(f"render_arc42_pages: page {page}")

    (out / "00_architecture_overview.md").write_text(overview_page(root), encoding="utf-8")

    images = root / "arc42" / "images"
    if images.is_dir():
        shutil.copytree(images, out / "images", dirs_exist_ok=True)

    if failed:
        print(f"render_arc42_pages: {failed} section(s) failed")
        return 1
    print(f"render_arc42_pages: {len(sections)} section page(s) + overview in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
