#!/usr/bin/env python3
"""Gate a hand-numbered markdown doc: decimal heading numbers + anchor integrity.

Usage:
    python3 check_heading_numbering.py <doc.md> [<doc2.md> ...] [-r|--root DIR]

Checks, per document
    1. Every heading below the H1 title is numbered, with the number inside the same
       code span as the title, and its dot-group count equal to heading level - 1.
       Headings that precede the first numbered one are tolerated as the optional
       unnumbered scope section a rules doc may open with.
    2. Siblings run 1..N in document order (no gaps, no repeats under one parent).
    3. Every `](#anchor)` and `](other.md#anchor)` target exists among the regenerated
       GitHub/VSCode slugs of the target document's headings.

Fenced code blocks are skipped, so a `#define` line inside an example is not read as a
heading. Exit code 1 when any check fails, so it can gate a rules-doc change.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata

FENCE = re.compile(r"^\s*```")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
NUMBERED = re.compile(r"^`(\d+(?:\.\d+)*)\.\s+\S.*`$")
LINK = re.compile(r"\]\(([^)\s]+)\)")
EXTERNAL = ("http://", "https://", "mailto:", "data:", "#!")


def headings(text: str) -> list[tuple[int, int, str]]:
    """Return (line_number, level, text) for headings outside fenced code blocks."""
    found, in_fence = [], False
    for lineno, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING.match(line)
        if match:
            found.append((lineno, len(match.group(1)), match.group(2).strip()))
    return found


def slug(text: str) -> str:
    """GitHub/VSCode heading slug: lowercase, punctuation dropped, spaces hyphenated."""
    flat = unicodedata.normalize("NFKD", text).lower()
    flat = re.sub(r"[^\w\s-]", "", flat)
    return re.sub(r"\s", "-", flat)


def check(path: str, root: str | None) -> list[str]:
    text = open(path, encoding="utf-8").read()
    heads = headings(text)
    problems: list[str] = []

    title = heads[0] if heads and heads[0][1] == 1 else None
    body = [h for h in heads if h is not title]

    last_child: dict[tuple[int, ...], int] = {}
    scope_section = True          # an unnumbered scope section may open the document
    for lineno, level, heading in body:
        match = NUMBERED.match(heading)
        if not match:
            if scope_section:
                continue          # headings before the first numbered one
            problems.append(
                f"{path}:{lineno}: heading not numbered inside one code span: {heading!r}")
            continue
        scope_section = False
        number = [int(part) for part in match.group(1).split(".")]
        if len(number) != level - 1:
            problems.append(
                f"{path}:{lineno}: {len(number)} dot-group(s) on an H{level} heading, "
                f"expected {level - 1}: {heading!r}")
        parent = tuple(number[:-1])
        expected = last_child.get(parent, 0) + 1
        if number[-1] != expected:
            where = "/".join(str(p) for p in parent) or "-"
            problems.append(
                f"{path}:{lineno}: expected sibling {where}.{expected}, "
                f"found {where}.{number[-1]}: {heading!r}")
        last_child[parent] = number[-1]

    slugs = {slug(heading) for _, _, heading in heads}
    for target in LINK.findall(text):
        if target.startswith(EXTERNAL) or "#" not in target:
            continue  # plain relative links are verify_rule_docs.py's job
        file_part, _, anchor = target.partition("#")
        file_part = file_part.strip("<>")
        if not file_part:
            if anchor not in slugs:
                problems.append(f"{path}: dead in-page anchor: #{anchor}")
            continue
        other = os.path.normpath(
            os.path.join(root or os.path.dirname(path) or ".", file_part))
        if not os.path.exists(other):
            problems.append(f"{path}: anchor link to a missing file: {target}")
            continue
        other_slugs = {slug(h) for _, _, h in
                       headings(open(other, encoding="utf-8").read())}
        if anchor not in other_slugs:
            problems.append(f"{path}: dead anchor in {other}: #{anchor}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="+", help="markdown documents to check")
    parser.add_argument("-r", "--root", default=None,
                        help="directory relative anchor links resolve against "
                             "(default: the document's own directory)")
    args = parser.parse_args()

    failed = False
    for path in args.files:
        problems = check(path, args.root)
        if problems:
            failed = True
            for problem in problems:
                print("FAIL " + problem)
        else:
            count = len(headings(open(path, encoding="utf-8").read()))
            print(f"ok   {path}: {count} heading(s) numbered, anchors resolve")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
