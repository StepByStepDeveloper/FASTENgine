#!/usr/bin/env python3
"""Report specification traceability: criteria, tests and gaps.

Collects the identifiers defined under ``docs/specs`` (``FR`` / ``NFR`` /
``AC`` / ``T``) and the traceability aliases — ``@covers{...}`` and
``@implements{...}`` — from the implementation roots, writes the report to
``build/trace/report.md`` and prints a summary. The workflow the report serves
is ``docs/development/conventions/process.md``.

Usage:
    python3 tools/trace.py [SPECS_DIR] [--roots DIR ...] [--out OUT_DIR]

Defaults: SPECS_DIR ``docs/specs``; roots ``src`` and ``tests`` (a root that
does not exist is skipped and reported); OUT_DIR ``build/trace``. Run from the
repository root.

Exit codes: 0 = report written, no problems; 1 = problems: a reference to an
identifier no specification defines, or an *Implemented* specification with an
uncovered acceptance criterion; 2 = the specifications directory is missing.

Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SPECS_DIR = Path("docs/specs")
DEFAULT_ROOTS = ("src", "tests")
DEFAULT_OUT = Path("build/trace")
SOURCE_SUFFIXES = (".hpp", ".cpp", ".h", ".cc")

SPEC_DIR_RE = re.compile(r"^(\d{3})-[a-z0-9-]+$")
TITLE_RE = re.compile(r"^= Spec (\d{3}): (.+)$", re.M)
STATUS_RE = re.compile(r"^:status:[ \t]*(.*?)[ \t]*$", re.M)
REQUIREMENT_RE = re.compile(r"^\* (FR|NFR)-(\d{3})-(\d{2})\b", re.M)
CRITERION_RE = re.compile(r"^\* AC-(\d{3})-(\d{2})\b", re.M)
TASK_TOKEN_RE = re.compile(r"\bT-\d{3}-\d{2}\b")
ALIAS_RE = re.compile(r"@(covers|implements)\{([^}]*)\}")
IDENTIFIER_RE = re.compile(r"\b((?:FR|NFR|AC|T)-\d{3}-\d{2})\b")

problems: list[str] = []
notes: list[str] = []


def problem(message: str) -> None:
    """Record one failing check item."""
    problems.append(message)


def note(message: str) -> None:
    """Record one item that is fine but worth naming in the summary."""
    notes.append(message)


@dataclass
class Specification:
    """One specification directory, reduced to what a trace can use."""

    directory: str
    number: str
    title: str
    status: str
    requirements: list[str] = field(default_factory=list)
    criteria: list[str] = field(default_factory=list)
    tasks: list[str] = field(default_factory=list)


def collect_specs(root: Path) -> list[Specification]:
    """The specifications under ``root``; a spec without spec.adoc is a note."""
    specs: list[Specification] = []
    for path in sorted(root.iterdir()):
        match = SPEC_DIR_RE.fullmatch(path.name)
        if not path.is_dir() or match is None:
            continue
        spec_file = path / "spec.adoc"
        if not spec_file.is_file():
            note(f"{path.name}: spec.adoc is missing — the directory is not traced")
            continue
        text = spec_file.read_text(encoding="utf-8")
        title = TITLE_RE.search(text)
        status = STATUS_RE.search(text)
        status_word = status.group(1).split() if status and status.group(1).split() else []
        tasks_file = path / "tasks.adoc"
        tasks_text = tasks_file.read_text(encoding="utf-8") if tasks_file.is_file() else ""
        specs.append(Specification(
            directory=path.name,
            number=match.group(1),
            title=title.group(2).strip() if title else "(untitled)",
            status=status_word[0] if status_word else "Unknown",
            requirements=[f"{kind}-{number}-{item}" for kind, number, item
                          in REQUIREMENT_RE.findall(text)],
            criteria=[f"AC-{number}-{item}" for number, item in CRITERION_RE.findall(text)],
            tasks=TASK_TOKEN_RE.findall(tasks_text),
        ))
    return specs


def scan_roots(roots: list[Path]) -> tuple[dict[str, list[tuple[str, str]]], list[tuple[str, int | None]]]:
    """Every ``@covers`` / ``@implements`` reference under the roots.

    Returns ``({"ID": [(kind, "path:line"), ...]}, [(root, file count)])``;
    a root that does not exist is reported with a ``None`` file count.
    """
    references: dict[str, list[tuple[str, str]]] = {}
    report: list[tuple[str, int | None]] = []
    for root in roots:
        if not root.is_dir():
            report.append((root.as_posix(), None))
            continue
        files = sorted(path for path in root.rglob("*")
                       if path.is_file() and path.suffix in SOURCE_SUFFIXES)
        for path in files:
            text = path.read_text(encoding="utf-8", errors="replace")
            for match in ALIAS_RE.finditer(text):
                kind = match.group(1)
                line = text.count("\n", 0, match.start()) + 1
                for identifier in IDENTIFIER_RE.findall(match.group(2)):
                    references.setdefault(identifier, []).append(
                        (kind, f"{path.as_posix()}:{line}"))
        report.append((root.as_posix(), len(files)))
    return references, report


def is_covered(references: dict[str, list[tuple[str, str]]], criterion: str) -> bool:
    """True when at least one ``@covers`` reference names this criterion."""
    return any(kind == "covers" for kind, _ in references.get(criterion, []))


def write_report(out_dir: Path, specs: list[Specification],
                 references: dict[str, list[tuple[str, str]]],
                 roots_report: list[tuple[str, int | None]],
                 dangling: list[str]) -> Path:
    """Write ``report.md`` into ``out_dir`` and return its path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    report = out_dir / "report.md"
    lines = [
        "# Traceability report",
        "",
        "Generated by `python3 tools/trace.py` from `docs/specs` and the "
        "implementation roots — a build artifact, not committed.",
        "",
    ]
    if specs:
        lines += [
            "## Coverage by specification",
            "",
            "| Specification | Status | Criteria | Covered | Uncovered |",
            "|:--|:--|--:|--:|:--|",
        ]
        for spec in specs:
            uncovered = [criterion for criterion in spec.criteria
                         if not is_covered(references, criterion)]
            lines.append(
                f"| {spec.directory} | {spec.status} | {len(spec.criteria)} | "
                f"{len(spec.criteria) - len(uncovered)} | {', '.join(uncovered) or '—'} |")
        lines += ["", "## References by identifier", "",
                  "| Identifier | `@covers` | `@implements` |", "|:--|--:|--:|"]
        for spec in specs:
            for identifier in spec.requirements + spec.criteria:
                kinds = [kind for kind, _ in references.get(identifier, [])]
                lines.append(f"| {identifier} | {kinds.count('covers')} | "
                             f"{kinds.count('implements')} |")
        lines.append("")
    else:
        lines += ["No specifications yet — the tree is in its declared empty state.", ""]

    lines += ["## Dangling references", ""]
    if dangling:
        lines += [f"- {message}" for message in dangling]
    else:
        lines.append("None — every `@covers` / `@implements` names an identifier "
                     "defined under `docs/specs/`.")
    lines += ["", "## Sources scanned", ""]
    for name, count in roots_report:
        lines.append(f"- `{name}` — " + (f"{count} file(s)" if count is not None
                                         else "not present"))
    lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("specs_dir", nargs="?", default=str(SPECS_DIR),
                        help="the specifications (default: docs/specs)")
    parser.add_argument("--roots", nargs="+", type=Path, default=list(DEFAULT_ROOTS),
                        metavar="DIR", help="implementation roots (default: src tests)")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help="report directory (default: build/trace)")
    args = parser.parse_args()

    root = Path(args.specs_dir)
    if not root.is_dir():
        print(f"trace: specifications directory not found: {root}")
        return 2

    specs = collect_specs(root)
    known = set()
    for spec in specs:
        known.update(spec.requirements)
        known.update(spec.criteria)
        known.update(spec.tasks)
    references, roots_report = scan_roots([Path(root) for root in args.roots])

    dangling = []
    for identifier in sorted(references):
        if identifier not in known:
            locations = references[identifier]
            dangling.append(f"{locations[0][1]} — `{identifier}` is referenced "
                            f"{len(locations)} time(s) but defined nowhere")
    problems.extend(dangling)

    for spec in specs:
        if spec.status not in ("Implementing", "Implemented") or not spec.criteria:
            continue
        uncovered = [criterion for criterion in spec.criteria
                     if not is_covered(references, criterion)]
        if uncovered:
            message = (f"{spec.directory} ({spec.status}): "
                       f"{len(spec.criteria) - len(uncovered)}/{len(spec.criteria)} "
                       f"criteria covered — uncovered: {', '.join(uncovered)}")
            (problem if spec.status == "Implemented" else note)(message)

    report = write_report(args.out, specs, references, roots_report, dangling)

    for message in notes:
        print(f"trace: note: {message}")
    for message in problems:
        print(f"trace: PROBLEM: {message}")
    print(f"trace: {'PASS' if not problems else 'CHECK'} — report: {report} "
          f"({len(problems)} problem(s), {len(notes)} note(s))")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
