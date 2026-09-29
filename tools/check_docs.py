#!/usr/bin/env python3
"""Check the documentation tree under docs/ against its conventions.

The conventions are binding in .agents/rules/docs.md; this script is their
mechanical half for the document tree itself. Checks:

  sections   the twelve section files exist, and the master includes each
             exactly once, in order
  includes   every ``include::`` target under docs/ resolves
  adrs       file names, numbering (contiguous from 0001), anchors, titles and
             ``Status: <status> (<YYYY-MM-DD>).`` lines
  regions    the two generated regions of Section 9 match the ADR files on disk
  images     every ``image::`` reference resolves to a file, or to a diagram
             source that ``doit diagrams`` renders into it
  links      every relative ``xref:`` / ``link:`` target resolves

Usage:
    python3 tools/check_docs.py [--root docs]

Exit codes: 0 = every check passed, 1 = at least one check reported a problem,
2 = the docs root does not exist.

Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
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

ADR_FILE_RE = re.compile(r"^\d{4}-[a-z0-9-]+\.adoc$")
ANCHOR_RE = re.compile(r"^\[\[adr-(\d{4})\]\][ \t]*$", re.M)
TITLE_RE = re.compile(r"^= ADR-(\d{4}): (.+)$", re.M)
STATUS_RE = re.compile(r"^Status: (.+?) \((\d{4}-\d{2}-\d{2})\)\.[ \t]*$", re.M)
INDEX_ROW_RE = re.compile(
    r"^\| <<adr-(\d{4}),ADR-\d{4}>> \| (.+?) \| (.+?) \| (\d{4}-\d{2}-\d{2})$", re.M
)
INCLUDE_RE = re.compile(r"^include::(.+?)\[\]$", re.M)
INCLUDE_REGION_RE = re.compile(r"^include::\.\./adr/(.+?)\[\]$", re.M)
IMAGE_RE = re.compile(r"^image::([^\s\[]+)\[", re.M)
LINK_RE = re.compile(r"(?:xref|link):([^\s\[]+)\[")
STATUS_WORDS = ("proposed", "accepted", "rejected", "deprecated", "superseded")

problems: list[str] = []
notes: list[str] = []


def problem(message: str) -> None:
    """Record one failing check item."""
    problems.append(message)


def note(message: str) -> None:
    """Record one item that is fine but worth naming in the summary."""
    notes.append(message)


def region(text: str, start: str, end: str) -> str:
    """The lines strictly between two marker comments (``""`` when absent)."""
    if start not in text or end not in text:
        return ""
    return text.split(start, 1)[1].split(end, 1)[0]


def adoc_files(root: Path) -> list[Path]:
    """Every AsciiDoc source under the docs root."""
    return sorted(root.rglob("*.adoc"))


def check_sections(root: Path) -> None:
    """The twelve section files exist and the master includes them, in order."""
    arc42 = root / "arc42"
    master = arc42 / "arc42.adoc"
    if not master.is_file():
        problem(f"missing master document: {master}")
        return
    for stem in SECTION_STEMS:
        path = arc42 / "sections" / f"{stem}.adoc"
        if not path.is_file():
            problem(f"missing section file: {path}")
    includes = [target for target in INCLUDE_RE.findall(master.read_text(encoding="utf-8"))
                if target.startswith("sections/")]
    expected = [f"sections/{stem}.adoc" for stem in SECTION_STEMS]
    if includes != expected:
        problem(f"the master must include sections/01..12 once, in order "
                f"(found {len(includes)} include(s))")


def check_includes(root: Path) -> None:
    """Every include:: target under docs/ resolves relative to its includer."""
    for path in adoc_files(root):
        for target in INCLUDE_RE.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "/")):
                continue
            if not (path.parent / target).resolve().exists():
                problem(f"{path}: include target does not resolve: {target}")


def parse_adr(path: Path) -> dict | None:
    """One ADR parsed to ``{number, title, status, date, file}``, or None + problem."""
    text = path.read_text(encoding="utf-8")
    anchor = ANCHOR_RE.search(text)
    title = TITLE_RE.search(text)
    status = STATUS_RE.search(text)
    if anchor is None or title is None:
        problem(f"{path.name}: missing '[[adr-NNNN]]' anchor or '= ADR-NNNN: ' title line")
        return None
    if anchor.group(1) != title.group(1) or path.name[:4] != title.group(1):
        problem(f"{path.name}: the number in the file name, anchor and title must agree")
        return None
    if status is None:
        problem(f"{path.name}: missing 'Status: <status> (<YYYY-MM-DD>).' line")
        return None
    word = status.group(1).split()[0]
    if word not in STATUS_WORDS or (word == "superseded"
                                    and not re.fullmatch(r"superseded by ADR-\d{4}", status.group(1))):
        problem(f"{path.name}: unknown status '{status.group(1)}'")
        return None
    return {"number": int(title.group(1)), "title": title.group(2).strip(),
            "status": status.group(1).strip(), "date": status.group(2), "file": path.name}


def check_adrs(root: Path) -> list[dict]:
    """The ADR set: names, numbering, anchors, titles, Status lines."""
    adr_dir = root / "arc42" / "adr"
    if not (adr_dir / "adr-template.adoc").is_file():
        problem(f"missing ADR template: {adr_dir / 'adr-template.adoc'}")
    files = sorted(p for p in adr_dir.iterdir() if ADR_FILE_RE.match(p.name))
    adrs = [parsed for parsed in (parse_adr(p) for p in files) if parsed is not None]
    numbers = [adr["number"] for adr in adrs]
    if numbers != list(range(1, len(numbers) + 1)):
        problem(f"ADR numbering must be contiguous from 0001 (found {numbers})")
    return adrs


def check_regions(root: Path, adrs: list[dict]) -> None:
    """The generated regions of Section 9 match the ADR files on disk."""
    section = root / "arc42" / "sections" / "09_architecture_decisions.adoc"
    if not section.is_file():
        return
    text = section.read_text(encoding="utf-8")
    rows = INDEX_ROW_RE.findall(region(text, "// adr-index-start", "// adr-index-end"))
    included = INCLUDE_REGION_RE.findall(region(text, "// adr-include-start", "// adr-include-end"))
    expected_rows = [(f"{adr['number']:04d}", adr["title"], adr["status"], adr["date"])
                     for adr in sorted(adrs, key=lambda adr: adr["number"])]
    expected_includes = [adr["file"] for adr in sorted(adrs, key=lambda adr: adr["number"])]
    if rows != expected_rows:
        problem("the Section 9 index region does not match the ADR files — "
                "run: python3 tools/new_adr.py --regenerate")
    if included != expected_includes:
        problem("the Section 9 include region does not match the ADR files — "
                "run: python3 tools/new_adr.py --regenerate")


def check_images(root: Path) -> None:
    """Every image:: reference resolves to a file or to a diagram source."""
    arc42 = root / "arc42"
    for path in adoc_files(root):
        for target in IMAGE_RE.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "/")):
                continue
            candidates = [path.parent / target, arc42 / target, arc42 / "images" / target]
            if any(candidate.resolve().is_file() for candidate in candidates):
                continue
            stem = Path(target).stem
            if (arc42 / "diagrams" / f"{stem}.puml").is_file():
                note(f"{path.name}: image '{target}' is a diagram render (doit diagrams)")
                continue
            problem(f"{path}: image reference resolves to neither a file "
                    f"nor a diagrams/{stem}.puml source: {target}")


def check_links(root: Path) -> None:
    """Every relative xref:/link: target resolves (the file part, at least)."""
    for path in adoc_files(root):
        for target in LINK_RE.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            if not (path.parent / clean).resolve().exists():
                problem(f"{path}: link target does not resolve: {target}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", default="docs", help="the documentation root (default: docs)")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"check_docs: docs root not found: {root}")
        return 2

    check_sections(root)
    check_includes(root)
    adrs = check_adrs(root)
    check_regions(root, adrs)
    check_images(root)
    check_links(root)

    for message in notes:
        print(f"check_docs: note: {message}")
    for message in problems:
        print(f"check_docs: PROBLEM: {message}")
    print(f"check_docs: {'PASS' if not problems else 'CHECK'} — "
          f"{len(problems)} problem(s), {len(notes)} note(s)")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
