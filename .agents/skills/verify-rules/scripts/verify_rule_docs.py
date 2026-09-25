#!/usr/bin/env python3
"""Verify a repository's rules documentation tree.

Two checks, both of which catch defects a human review misses:

1. Snippet compilation -- every fenced code block of a compilable language is
extracted and compiled with warnings enabled. Blocks are compiled PER MARKDOWN
FILE by default: sibling rule docs routinely illustrate the same entity names (a
sample class appears in both the naming doc and the documentation doc), so
aggregating the whole tree into one translation unit reports duplicate-definition
errors that are not snippet defects. `--group tree` aggregates anyway, for a tree that
keeps each illustrative entity in exactly one document. Document that reuses one sample
type across its own examples (the same `IS_Drawable` declared in Example 4 and again in
Example 5): compile those fences with `--group block`, one translation unit per fence --
that is the only mode in which such a document can be green.
2. Relative link resolution -- every relative markdown link in the tree must
resolve to a file that exists.

Usage:
    python3 verify_rule_docs.py <rules-dir> [--group file|tree|block] [--compiler g++]
                                   [--std c++20]
                                   [--prelude '#include <cstddef>']

Exit code 0 only when every check passes. Stdlib only.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

SKIP_DIRS = {".git", ".obsidian", "node_modules", "__pycache__"}

# fenced block: ```lang[extra]
FENCE_RE = re.compile(r"```([A-Za-z0-9+#._-]*)[^\n]*\n(.*?)```", re.S)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+?)\)")

# language tag -> (source extension, compile kind)
LANGUAGES = {
    "c++": ("cpp", "c++"),
    "cpp": ("cpp", "c++"),
    "cxx": ("cpp", "c++"),
    "c": ("c", "c"),
    "py": ("py", "python"),
    "python": ("py", "python"),
}


def markdown_files(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)


def fence_blocks(path: str) -> dict[str, list[tuple[int, str]]]:
    """``{lang: [(first_line, body), ...]}`` for one markdown file."""
    text = open(path, encoding="utf-8").read()
    found: dict[str, list[tuple[int, str]]] = {}
    for match in FENCE_RE.finditer(text):
        lang = match.group(1).strip().lower()
        body = match.group(2)
        if not lang or not body.strip():
            continue
        first_line = text[: match.start()].count("\n") + 1
        found.setdefault(lang, []).append((first_line, body))
    return found


def compile_units(root: str, group: str):
    """Return ``[(label, lang, [(path, line, body), ...]), ...]`` to compile."""
    if group == "tree":
        merged: dict[str, list[tuple[str, int, str]]] = {}
        for path in markdown_files(root):
            for lang, blocks in fence_blocks(path).items():
                merged.setdefault(lang, []).extend((path, line, body) for line, body in blocks)
        return [(f"<tree> [{lang}]", lang, blocks) for lang, blocks in sorted(merged.items())]

    units = []
    for path in markdown_files(root):
        rel = os.path.relpath(path, root)
        for lang, blocks in sorted(fence_blocks(path).items()):
            if group == "block":
                units.extend(
                    (f"{rel}:{line}", lang, [(path, line, body)]) for line, body in blocks
                )
                continue
            units.append(
                (rel, lang, [(path, line, body) for line, body in blocks])
            )
    return units


def compile_command(kind: str, compiler: str, std: str, target: str):
    obj = target + ".o"
    if kind == "c++":
        return [compiler, f"-std={std}", "-Wall", "-Wextra", "-Wpedantic", "-c", target, "-o", obj]
    if kind == "c":
        return [compiler, "-Wall", "-Wextra", "-c", target, "-o", obj]
    if kind == "python":
        return [sys.executable, "-m", "py_compile", target]
    return None


def check_snippets(root: str, compiler: str, std: str, prelude: str, group: str) -> bool:
    units = compile_units(root, group)
    if not units:
        print("snippets: none found (nothing to compile)")
        return True

    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        for index, (label, lang, blocks) in enumerate(units):
            info = LANGUAGES.get(lang)
            if info is None:
                print(
                    f"snippets [{label}]: skipped ({len(blocks)} block(s), "
                    "no compile check defined for this language)"
                )
                continue

            ext, kind = info
            target = os.path.join(tmp, f"unit_{index}.{ext}")
            source = (prelude + "\n" if kind == "c++" else "") + "\n\n".join(
                body for _, _, body in blocks
            ) + "\n"
            open(target, "w", encoding="utf-8").write(source)

            where = ", ".join(f"{os.path.relpath(p, root)}:{line}" for p, line, _ in blocks)
            cmd = compile_command(kind, compiler, std, target)
            if cmd is None or shutil.which(cmd[0]) is None:
                print(
                    f"snippets [{label}]: {len(blocks)} block(s) from {where} written to "
                    "a temp file but not compiled (no toolchain on PATH) -- report this "
                    "as unverified, not as passing"
                )
                continue

            proc = subprocess.run(cmd, capture_output=True, text=True)
            if proc.returncode != 0:
                ok = False
                print(f"snippets [{label}]: FAIL ({len(blocks)} block(s) from {where})")
                print(proc.stdout + proc.stderr)
                continue

            diagnostics = [ln for ln in (proc.stdout + proc.stderr).splitlines() if ln.strip()]
            if diagnostics:
                print(
                    f"snippets [{label}]: compiles with {len(diagnostics)} diagnostic line(s) "
                    f"({where}) -- quote them in your report, never call it clean"
                )
                for ln in diagnostics[:20]:
                    print("   " + ln)
            else:
                print(f"snippets [{label}]: OK, no warnings ({len(blocks)} block(s) from {where})")
    return ok


def check_links(root: str) -> bool:
    broken = []
    checked = 0
    for path in markdown_files(root):
        text = open(path, encoding="utf-8").read()
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            checked += 1
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), clean))
            if not os.path.exists(resolved):
                broken.append((path, target))
    if broken:
        print(f"links: {len(broken)} broken of {checked} relative link(s)")
        for path, target in broken:
            print(f"   {path} -> {target}")
        return False
    print(f"links: OK, {checked} relative link(s) resolved")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rules_dir", help="root of the rules tree, e.g. <repo>/.agents/rules")
    parser.add_argument(
        "--group",
        choices=("file", "tree", "block"),
        default="file",
        help="compile each markdown file's blocks on their own (default), merge the whole "
        "tree, or compile every fence as its own unit",
    )
    parser.add_argument("--compiler", default="g++")
    parser.add_argument("--std", default="c++20")
    parser.add_argument(
        "--prelude",
        default="#include <cstddef>\n#include <cstdint>\n",
        help="header prelude prepended to the concatenated C++ snippets",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.rules_dir):
        print(f"rules dir not found: {args.rules_dir}")
        return 2

    snippets_ok = check_snippets(
        args.rules_dir, args.compiler, args.std, args.prelude, args.group
    )
    links_ok = check_links(args.rules_dir)
    print("result:", "PASS" if (snippets_ok and links_ok) else "FAIL")
    return 0 if (snippets_ok and links_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
