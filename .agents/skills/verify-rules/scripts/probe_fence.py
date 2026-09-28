#!/usr/bin/env python3
"""Dump a fenced code block of a markdown doc as a standalone file (probe helper).

Usage:
  python3 probe_fence.py <doc.md> [--lang C++] [--index N] [--out FILE]

Default picks the LARGEST block of the requested language, which is what a doc's
self-contained "ultimate example" is. --index N selects the N-th block (0-based,
document order) when you need one of the small examples instead.

Exit 0 on success; a missing block or an out-of-range --index exits 1 with a message.
"""

import argparse
import sys


def blocks(text, lang):
    """Return every fenced block whose info string equals `lang`."""
    found, current, inside = [], [], False
    for line in text.splitlines():
        stripped = line.strip()
        if inside and stripped == "```":
            found.append(current)
            current, inside = [], False
            continue
        if inside:
            current.append(line)
            continue
        if stripped.startswith("```") and stripped[3:].strip() == lang:
            inside = True
    if inside:  # unterminated fence: keep what was collected
        found.append(current)
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("doc")
    parser.add_argument("--lang", default="C++")
    parser.add_argument("--index", type=int, help="0-based block index")
    parser.add_argument("--out", default="probe_fence.cpp")
    args = parser.parse_args()

    with open(args.doc, encoding="utf-8") as handle:
        found = blocks(handle.read(), args.lang)
    if not found:
        sys.exit(f"no ```{args.lang} block in {args.doc}")

    index = args.index if args.index is not None else max(range(len(found)), key=lambda k: len(found[k]))
    if not 0 <= index < len(found):
        sys.exit(f"--index {index} out of range: {len(found)} block(s)")

    block = found[index]
    with open(args.out, "w", encoding="utf-8") as handle:
        handle.write("\n".join(block) + "\n")
    print(f"{args.out}: {len(block)} lines, block {index} of {len(found)}")


if __name__ == "__main__":
    main()
