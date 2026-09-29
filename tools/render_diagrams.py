#!/usr/bin/env python3
"""Render the PlantUML diagram sources of the architecture documentation.

Every ``docs/arc42/diagrams/*.puml`` becomes ``docs/arc42/images/<name>.svg``
through the PlantUML renderer (see .agents/docs/toolchain.md). Renders are
build artifacts: they are not committed, and the documents reference the SVG
name, never the .puml (see .agents/rules/docs.md).

Usage:
    python3 tools/render_diagrams.py [--force] [--root docs]

``--force`` re-renders even when the SVG is newer than its source. Without it,
up-to-date renders are skipped.

Exit codes: 0 = every render is fresh (or there are no sources); 1 = a render
failed; 2 = no PlantUML renderer on PATH, or the docs root does not exist.

Standard library only.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--force", action="store_true",
                        help="re-render even when the SVG is newer than its source")
    parser.add_argument("--root", default="docs", help="the documentation root (default: docs)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"render_diagrams: docs root not found: {root}")
        return 2

    renderer = shutil.which("plantuml")
    if renderer is None:
        print("render_diagrams: no 'plantuml' on PATH — see .agents/docs/toolchain.md "
              "for the renderer this repository expects")
        return 2

    sources = sorted((root / "arc42" / "diagrams").glob("*.puml"))
    if not sources:
        print("render_diagrams: no diagram sources yet (docs/arc42/diagrams/*.puml)")
        return 0

    images = (root / "arc42" / "images").resolve()
    images.mkdir(parents=True, exist_ok=True)

    failed = 0
    for source in sources:
        target = images / f"{source.stem}.svg"
        if target.is_file() and not args.force and target.stat().st_mtime >= source.stat().st_mtime:
            print(f"render_diagrams: up to date: {target.relative_to(root.parent)}")
            continue
        proc = subprocess.run(
            [renderer, "-tsvg", "-charset", "UTF-8", "-o", str(images), str(source)],
            capture_output=True, text=True,
        )
        if proc.returncode != 0 or not target.is_file():
            failed += 1
            print(f"render_diagrams: FAILED: {source}")
            print(proc.stdout + proc.stderr)
            continue
        print(f"render_diagrams: rendered {source} -> {target.relative_to(root.parent)}")

    if failed:
        print(f"render_diagrams: {failed} render(s) failed")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
