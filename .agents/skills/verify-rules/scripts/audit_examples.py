#!/usr/bin/env python3
"""Audit one markdown doc's fenced C++ examples against the claims its folder makes.

Per fence: compile it standalone with NO prelude and again with a minimal one, on
every compiler passed, with -Wall -Wextra -Wpedantic and a real `-c` build (a
-fsyntax-only run drops codegen-only warning classes under GCC). Census fenced
line lengths; print each comment block's star and text columns so a continuation
line that does not align with its tag is visible. Then build the whole document
as one translation unit (the promise these docs usually make) and count
retired/new tokens.

Usage:
  python3 audit_examples.py <doc.md> [--std c++17] [--compilers clang++,g++]
                            [--max-line 120] [--retired tok,tok] [--new tok,tok]
                            [--prelude '#include <cstddef>\n#include <cstdint>']

Exit 0 when nothing produces a compiler error; warnings are reported, never
fatal, because an illustrative fragment may legitimately declare names nothing
reads (say which front end warns in the report).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

FLAGS = ["-Wall", "-Wextra", "-Wpedantic"]


def fences(text: str):
    """(first_body_line, body) per fence. State machine, not a regex: an opener
    pattern that also matches a bare closer desynchronizes the parse, and a tag
    carrying punctuation (```C++) is not `\\w+`."""
    out, body, start, inside = [], [], 0, False
    for i, line in enumerate(text.split("\n"), 1):
        if not inside:
            if line.lstrip().startswith("```"):
                inside, body, start = True, [], i + 1
        elif line.strip() == "```":
            out.append((start, "\n".join(body)))
            inside = False
        else:
            body.append(line)
    assert not inside, "file ends inside a fence"
    return out


def compile_src(src: str, compiler: str, std: str, prelude: str):
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "probe.cpp"
        target.write_text(prelude + src + "\n", encoding="utf-8")
        proc = subprocess.run(
            [compiler, f"-std={std}", *FLAGS, "-c", str(target), "-o", str(target) + ".o"],
            capture_output=True, text=True,
        )
    diag = [line.strip() for line in proc.stderr.split("\n") if line.strip()]
    return proc.returncode, diag


def comment_columns(body: str):
    """(line, marker_col, text_col, kind) for every comment line of the fence.
    kind=tag for a line whose text opens with @ or <. Read the columns: the
    checker must not guess whether a continuation is aligned, only show it."""
    rows, in_block = [], False
    for i, line in enumerate(body.split("\n"), 1):
        stripped = line.lstrip()
        if not in_block and "/**" in line:
            in_block = True
        if in_block:
            star = line.find("*")
            rest = line[star + 1:] if star >= 0 else ""
            text = rest.strip()
            text_col = star + 1 + (len(rest) - len(rest.lstrip())) if text else -1
            kind = "tag" if text.startswith(("@", "<")) else "text"
            rows.append((i, star, text_col, kind))
            if "*/" in rest:
                in_block = False
        elif stripped.startswith("///"):
            slash = line.index("///")
            rest = line[slash + 3:]
            text = rest.strip()
            text_col = slash + 3 + (len(rest) - len(rest.lstrip())) if text else -1
            kind = "tag" if text.startswith(("@", "<")) else "text"
            rows.append((i, slash, text_col, kind))
    return rows


def report(label: str, compiler: str, tag: str, src: str, std: str, prelude: str):
    rc, diag = compile_src(src, compiler, std, prelude)
    errs = [d for d in diag if "error:" in d]
    warns = [d for d in diag if "warning:" in d]
    print(f"   {Path(compiler).name:14s} {tag:8s} rc={rc} errors={len(errs)} warnings={len(warns)}")
    for d in (errs + warns)[:4]:
        print(f"      {d}")
    return len(errs)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("doc")
    ap.add_argument("--std", default="c++17")
    ap.add_argument("--compilers", default="clang++,g++")
    ap.add_argument("--max-line", type=int, default=120)
    ap.add_argument("--retired", default="")
    ap.add_argument("--new", default="")
    ap.add_argument("--prelude", default="#include <cstddef>\n#include <cstdint>")
    args = ap.parse_args()

    text = Path(args.doc).read_text(encoding="utf-8")
    compilers = [c for c in args.compilers.split(",") if c]
    for compiler in compilers:
        proc = subprocess.run([compiler, "--version"], capture_output=True, text=True)
        print(f"# {proc.stdout.splitlines()[0] if proc.stdout else compiler}")

    blocks = fences(text)
    print(f"== {args.doc}: {len(blocks)} fence(s), std={args.std} ==")
    errors = 0
    for start, body in blocks:
        lines = body.split("\n")
        long = [(start + i, len(line)) for i, line in enumerate(lines) if len(line) > args.max_line]
        print(f"\n-- fence @ {start} ({len(lines)} lines)")
        print(f"   lines > {args.max_line}: {long or 'none'}")
        for line_no, marker, text_col, kind in comment_columns(body):
            if kind == "text" and text_col >= 0:
                print(f"   comment line {start + line_no - 1}: marker col {marker}, text col {text_col}")
        for compiler in compilers:
            errors += report("", compiler, "bare", body, args.std, "")
            errors += report("", compiler, "prelude", body, args.std, args.prelude + "\n")

    print("\n-- whole document as one translation unit")
    whole = "\n\n".join(body for _, body in blocks)
    for compiler in compilers:
        errors += report("", compiler, "prelude", whole, args.std, args.prelude + "\n")
        errors += report("", compiler, "bare", whole, args.std, "")

    for label, tokens in (("retired", args.retired), ("new", args.new)):
        for token in [t for t in tokens.split(",") if t]:
            print(f"{label:8s} {token!r}: {text.count(token)} occurrence(s)")

    print("result:", "FAIL (errors above)" if errors else "OK (no compiler error)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
