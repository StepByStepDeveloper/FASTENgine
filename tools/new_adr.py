#!/usr/bin/env python3
"""Create an architecture decision record (ADR) and regenerate the decision index.

The ADR set lives in ``docs/arc42/adr/``. Section 9 of the arc42 document
(``docs/arc42/sections/09_architecture_decisions.adoc``) carries two generated
regions between marker comments — the index table and the include list — and
this script is their only writer.

Usage:
    python3 tools/new_adr.py "Title of the decision" [--status proposed]
    python3 tools/new_adr.py --regenerate
    python3 tools/new_adr.py --help

``--status`` picks the opening status word (see
docs/development/conventions/docs.md for the vocabulary). ``--regenerate`` rewrites the two regions from the ADR files on
disk without creating anything — run it after hand-editing an ADR's title or
status line.

Exit codes: 0 = written and consistent; 1 = a state error (missing template,
missing markers, duplicate file, malformed ADR, a title the index table cannot
carry); 2 = invalid arguments (argparse).

Standard library only.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

ADR_DIR = Path("docs/arc42/adr")
SECTIONS_FILE = Path("docs/arc42/sections/09_architecture_decisions.adoc")
TEMPLATE_FILE = ADR_DIR / "adr-template.adoc"

INDEX_START = "// adr-index-start"
INDEX_END = "// adr-index-end"
INCLUDE_START = "// adr-include-start"
INCLUDE_END = "// adr-include-end"

ADR_FILE_RE = re.compile(r"^\d{4}-[a-z0-9-]+\.adoc$")
ANCHOR_RE = re.compile(r"^\[\[adr-(\d{4})\]\][ \t]*$", re.M)
TITLE_RE = re.compile(r"^= ADR-(\d{4}): (.+)$", re.M)
STATUS_RE = re.compile(r"^Status: (.+?) \((\d{4}-\d{2}-\d{2})\)\.[ \t]*$", re.M)

STATUSES = ("proposed", "accepted", "rejected", "deprecated")


def fail(message: str) -> int:
    """Print one error line and return the state-error exit code."""
    print(f"new_adr: {message}")
    return 1


def parse_adr(path: Path) -> dict:
    """Read one ADR file into ``{number, title, status, date, file}``.

    Raises ``ValueError`` when the anchor, the title line or the Status line is
    missing or malformed — the index cannot be generated from such a file.
    """
    text = path.read_text(encoding="utf-8")
    anchor = ANCHOR_RE.search(text)
    title = TITLE_RE.search(text)
    status = STATUS_RE.search(text)
    if anchor is None or title is None:
        raise ValueError(f"{path.name}: missing '[[adr-NNNN]]' anchor or '= ADR-NNNN: ' title line")
    if anchor.group(1) != title.group(1):
        raise ValueError(f"{path.name}: anchor {anchor.group(1)} and title {title.group(1)} disagree")
    if status is None:
        raise ValueError(f"{path.name}: missing 'Status: <status> (<YYYY-MM-DD>).' line")
    return {
        "number": int(title.group(1)),
        "title": title.group(2).strip(),
        "status": status.group(1).strip(),
        "date": status.group(2),
        "file": path.name,
    }


def collect() -> list[dict]:
    """Every ADR file on disk, parsed and ordered by number."""
    adrs = [parse_adr(p) for p in sorted(ADR_DIR.iterdir()) if ADR_FILE_RE.match(p.name)]
    return sorted(adrs, key=lambda adr: adr["number"])


def index_block(adrs: list[dict]) -> str:
    """The full index table — the content of the index region."""
    rows = "\n".join(
        f"| <<adr-{adr['number']:04d},ADR-{adr['number']:04d}>>"
        f" | {adr['title']} | {adr['status']} | {adr['date']}"
        for adr in adrs
    )
    return "\n".join([
        '[options="header",cols="1,4,1,1"]',
        "|===",
        "| # | Title | Status | Date",
        rows,
        "|===",
    ])


def include_block(adrs: list[dict]) -> str:
    """The include list — the content of the include region.

    One blank line between the includes: an included ADR file ends without a
    trailing blank line, and Asciidoctor would otherwise glue the next ADR's
    title line into the previous paragraph — the title then never becomes a
    section (measured while converting the pages for Doxygen).
    """
    return "\n\n".join(f"include::../adr/{adr['file']}[]" for adr in adrs)


def replace_region(path: Path, start: str, end: str, content: str) -> None:
    """Replace the lines between two marker comments with ``content``."""
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if line.startswith(start)]
    ends = [i for i, line in enumerate(lines) if line.startswith(end)]
    if len(starts) != 1 or len(ends) != 1 or starts[0] > ends[0]:
        raise ValueError(f"{path}: expected exactly one '{start}' before one '{end}' marker")
    path.write_text(
        "\n".join(lines[: starts[0] + 1] + content.splitlines() + lines[ends[0]:]) + "\n",
        encoding="utf-8",
    )


def regenerate() -> None:
    """Rewrite both generated regions of Section 9 from the files on disk."""
    adrs = collect()
    replace_region(SECTIONS_FILE, INDEX_START, INDEX_END, index_block(adrs))
    replace_region(SECTIONS_FILE, INCLUDE_START, INCLUDE_END, include_block(adrs))
    print(f"new_adr: index regenerated from {len(adrs)} ADR file(s)")


def slugify(title: str) -> str:
    """A file-name slug: lowercase ASCII words joined by single hyphens."""
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("title", nargs="?", help="short title of the decision")
    parser.add_argument("--status", choices=STATUSES, default="proposed",
                        help="opening status word (default: proposed)")
    parser.add_argument("--regenerate", action="store_true",
                        help="rewrite the generated regions from the files on disk")
    args = parser.parse_args()

    if args.regenerate:
        return 0 if _run(regenerate) else 1
    if not args.title:
        parser.error("a title is required unless --regenerate is given")
    if "|" in args.title:
        return fail("a title containing '|' cannot be carried by the index table")

    return 0 if _run(lambda: create(args.title, args.status)) else 1


def _run(step) -> bool:
    """Run ``step``, reporting its state errors as a message and exit code 1."""
    try:
        step()
    except (ValueError, OSError) as error:
        fail(str(error))
        return False
    return True


def create(title: str, status: str) -> None:
    """Write a new ADR from the template, then regenerate the index regions."""
    if not TEMPLATE_FILE.is_file():
        raise ValueError(f"template not found: {TEMPLATE_FILE}")
    adrs = collect()
    number = max((adr["number"] for adr in adrs), default=0) + 1
    destination = ADR_DIR / f"{number:04d}-{slugify(title)}.adoc"
    if destination.exists():
        raise ValueError(f"already exists: {destination}")

    text = TEMPLATE_FILE.read_text(encoding="utf-8")
    text = (text
            .replace("[[adr-NNNN]]", f"[[adr-{number:04d}]]")
            .replace("= ADR-NNNN: <Title>", f"= ADR-{number:04d}: {title}")
            .replace("Status: <status> (<YYYY-MM-DD>).",
                     f"Status: {status} ({datetime.date.today().isoformat()})."))
    destination.write_text(text, encoding="utf-8")
    print(f"new_adr: created {destination}")
    regenerate()


if __name__ == "__main__":
    sys.exit(main())
