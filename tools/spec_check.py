#!/usr/bin/env python3
"""Validate the specifications under ``docs/specs/``.

The process artifacts live in ``docs/specs/``: one directory per specification,
``NNN-<slug>/``, carrying the planning package — ``spec.adoc``,
``plan.adoc`` and ``tasks.adoc``, all drafted before the review. The binding
rules are
``docs/development/conventions/process.md``; the templates are
``docs/specs/_templates/``.

The script checks what is mechanical about a specification set:

  structure    the directory name, the ``spec.adoc`` header (title,
               ``:status:``, ``:feature-id:``, ``:owner:``, ``:adr:``,
               ``:arc42:``) and the template's sections are present;
  identifiers  FR / NFR / AC / T identifiers are well-formed, are not defined
               twice inside a specification or across the tree, and every
               acceptance criterion names a requirement that exists;
  coverage     past *Draft*, every requirement is covered by at least one
               acceptance criterion, and no ``NEEDS CLARIFICATION`` remains;
  lifecycle    *Approved* and later specifications carry a plan and a task
               list — the review agrees the whole package — and the plan and
               the task list belong to their specification;
  links        every ADR named in ``:adr:`` exists under ``docs/arc42/adr/``.

Findings that break the template are *problems* (exit 1); a draft that is
still being written and style deviations are *notes* (exit 0).

Usage:
    python3 tools/spec_check.py [SPECS_DIR]

SPECS_DIR defaults to ``docs/specs``. Run from the repository root. Exit
codes: 0 = clean (notes may be printed); 1 = problems were reported;
2 = the specifications directory does not exist.

Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SPECS_DIR = Path("docs/specs")
ADR_DIR = Path("docs/arc42/adr")
TEMPLATES = ("spec.adoc", "plan.adoc", "tasks.adoc")

STATUSES = ("Draft", "Approved", "Implementing", "Implemented", "Superseded")
# Statuses at which the specification is a promise: completeness is enforced.
ENFORCED_STATUSES = ("Approved", "Implementing", "Implemented")
# Statuses that cannot exist without a plan and a task list: the planning
# package is complete once the review agrees it, at *Approved*.
PACKAGE_STATUSES = ("Approved", "Implementing", "Implemented")

TASK_STATUSES = ("todo", "doing", "done", "withdrawn")

SPEC_DIR_RE = re.compile(r"^(\d{3})-[a-z0-9-]+$")
TITLE_RE = re.compile(r"^= Spec (\d{3}|NNN): (.+)$", re.M)
PLAN_TITLE_RE = re.compile(r"^= Plan (\d{3}|NNN): (.+)$", re.M)
TASKS_TITLE_RE = re.compile(r"^= Tasks (\d{3}|NNN): (.+)$", re.M)
SECTION_RE = re.compile(r"^== (.+?)[ \t]*$", re.M)
SUBSECTION_RE = re.compile(r"^=== (.+?)[ \t]*$", re.M)
ATTR_RE = re.compile(r"^:([a-z0-9-]+):[ \t]*(.*?)[ \t]*$", re.M)
REQUIREMENT_RE = re.compile(r"^\* (FR|NFR)-(\d{3})-(\d{2})\b", re.M)
CRITERION_RE = re.compile(r"^\* AC-(\d{3})-(\d{2})\b", re.M)
CRITERION_REF_RE = re.compile(r"\(((?:FR|NFR)-\d{3}-\d{2})\)")
TASK_ID_RE = re.compile(r"^T-(\d{3})-(\d{2})$")
AC_TOKEN_RE = re.compile(r"\bAC-\d{3}-\d{2}\b")

REQUIRED_SECTIONS = (
    "Goal",
    "Context",
    "Non-goals",
    "Requirements",
    "Acceptance Criteria",
    "Constraints",
    "Open Questions",
    "Links",
)
REQUIRED_SUBSECTIONS = ("Functional", "Non-functional")

HEADER_ATTRIBUTES = ("status", "feature-id", "owner", "adr", "arc42")

problems: list[str] = []
notes: list[str] = []
# Every identifier defined anywhere in the tree, mapped to the first file that
# defined it — the second definition of the same identifier is a problem.
defined_ids: dict[str, str] = {}


def problem(message: str) -> None:
    """Record one failing check item."""
    problems.append(message)


def note(message: str) -> None:
    """Record one item that is fine but worth naming in the summary."""
    notes.append(message)


def unfilled(value: str) -> bool:
    """True while a field still carries a template placeholder."""
    return "<" in value and ">" in value


def line_of(text: str, position: int) -> str:
    """The full line that contains ``position``."""
    start = text.rfind("\n", 0, position) + 1
    end = text.find("\n", position)
    return text[start:end if end != -1 else len(text)]


def define_identifier(label: str, spec_id: str) -> None:
    """Record one identifier definition; a second definition is a problem."""
    first = defined_ids.get(spec_id)
    if first is None:
        defined_ids[spec_id] = label
    elif first == label:
        problem(f"{label}: identifier {spec_id} is defined more than once")
    else:
        problem(f"{label}: identifier {spec_id} is also defined in {first}")


def check_header(label: str, attrs: dict[str, str], status: str) -> None:
    """The document-header attributes of ``spec.adoc`` follow the template."""
    enforced = status in ENFORCED_STATUSES
    for name in HEADER_ATTRIBUTES:
        if name not in attrs:
            problem(f"{label}: ':{name}:' is missing from the header")

    feature = attrs.get("feature-id", "")
    if feature and not re.fullmatch(r"\d{3}", feature):
        (problem if enforced else note)(
            f"{label}: ':feature-id:' is not a three-digit number: {feature!r}")
    elif feature and feature != label[:3]:
        problem(f"{label}: ':feature-id:' is {feature}, the directory is {label[:3]}")

    for name in ("owner", "adr", "arc42"):
        value = attrs.get(name, "")
        if value and unfilled(value):
            (problem if enforced else note)(
                f"{label}: ':{name}:' still carries a template placeholder")

    adr = attrs.get("adr", "")
    if adr and not unfilled(adr) and adr.strip().lower() != "none":
        references = re.findall(r"ADR-(\d{4})", adr)
        if not references:
            problem(f"{label}: ':adr:' names no ADR-NNNN (use 'none' when none is needed)")
        for number in references:
            if not list(ADR_DIR.glob(f"{number}-*.adoc")):
                problem(f"{label}: ':adr:' names ADR-{number}, which does not exist under {ADR_DIR}/")


def check_sections(label: str, text: str) -> None:
    """The template's sections are present; extra or reordered ones are notes."""
    names = [match.group(1).strip() for match in SECTION_RE.finditer(text)]
    for required in REQUIRED_SECTIONS:
        if required not in names:
            problem(f"{label}: missing section '== {required}'")
    subsections = [match.group(1).strip() for match in SUBSECTION_RE.finditer(text)]
    for required in REQUIRED_SUBSECTIONS:
        if required not in subsections:
            problem(f"{label}: missing subsection '=== {required}'")
    present = [name for name in names if name in REQUIRED_SECTIONS]
    if present != [name for name in REQUIRED_SECTIONS if name in present]:
        note(f"{label}: sections are present but not in template order")
    for name in names:
        if name not in REQUIRED_SECTIONS:
            note(f"{label}: non-template section '== {name}'")


def check_requirements(label: str, text: str, number: str) -> dict[str, str]:
    """Every requirement definition; returns ``{id: line}``.

    A requirement whose line carries the word ``withdrawn`` is recorded but
    exempt from the coverage rule — identifiers are never reused.
    """
    requirements: dict[str, str] = {}
    for match in REQUIREMENT_RE.finditer(text):
        kind, spec_number, item = match.groups()
        spec_id = f"{kind}-{spec_number}-{item}"
        requirements[spec_id] = line_of(text, match.start())
        if spec_number != number:
            problem(f"{label}: {spec_id} carries another specification's number")
        define_identifier(label, spec_id)
    return requirements


def check_criteria(label: str, text: str, number: str, requirements: dict[str, str],
                   enforced: bool) -> set[str]:
    """Every acceptance criterion references a requirement; returns the covered set."""
    covered: set[str] = set()
    for match in CRITERION_RE.finditer(text):
        spec_number, item = match.groups()
        spec_id = f"AC-{spec_number}-{item}"
        line = line_of(text, match.start())
        if spec_number != number:
            problem(f"{label}: {spec_id} carries another specification's number")
        define_identifier(label, spec_id)

        reference = CRITERION_REF_RE.search(line)
        if reference is None:
            (problem if enforced else note)(
                f"{label}: {spec_id} has no '(FR-NNN-NN)' reference")
        elif reference.group(1) not in requirements:
            (problem if enforced else note)(
                f"{label}: {spec_id} references {reference.group(1)}, "
                "which this specification does not define")
        else:
            covered.add(reference.group(1))
        if not all(word in line.lower() for word in ("given", "when", "then")):
            note(f"{label}: {spec_id} is not in Given/when/then form")
    return covered


def check_plan_and_tasks(label: str, spec_dir: Path, number: str,
                         status: str) -> None:
    """``plan.adoc`` and ``tasks.adoc`` exist when the status demands them."""
    required_now = status in PACKAGE_STATUSES

    plan_path = spec_dir / "plan.adoc"
    if plan_path.is_file():
        title = PLAN_TITLE_RE.search(plan_path.read_text(encoding="utf-8"))
        if title is None:
            problem(f"{label}: plan.adoc: the title line '= Plan NNN: <title>' is missing")
        elif title.group(1) == "NNN":
            (problem if required_now else note)(
                f"{label}: plan.adoc still reads 'Plan NNN'")
        elif title.group(1) != number:
            problem(f"{label}: plan.adoc says Plan {title.group(1)} "
                    f"but the directory says {number}")
    elif required_now:
        problem(f"{label}: plan.adoc is required while the status is {status}")

    tasks_path = spec_dir / "tasks.adoc"
    if not tasks_path.is_file():
        if required_now:
            problem(f"{label}: tasks.adoc is required while the status is {status}")
        return
    tasks_text = tasks_path.read_text(encoding="utf-8")
    title = TASKS_TITLE_RE.search(tasks_text)
    if title is None:
        problem(f"{label}: tasks.adoc: the title line '= Tasks NNN: <title>' is missing")
    elif title.group(1) == "NNN":
        (problem if required_now else note)(
            f"{label}: tasks.adoc still reads 'Tasks NNN'")
    elif title.group(1) != number:
        problem(f"{label}: tasks.adoc says Tasks {title.group(1)} "
                f"but the directory says {number}")

    rows = 0
    for line in tasks_text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 5 or cells[0] in ("ID", "") or set(cells[0]) <= {"-"}:
            continue
        rows += 1
        task = TASK_ID_RE.fullmatch(cells[0])
        if task is None:
            note(f"{label}: tasks.adoc: row does not start with a T-NNN-NN "
                 f"identifier: {cells[0]!r}")
            continue
        spec_id = f"T-{task.group(1)}-{task.group(2)}"
        if task.group(1) != number:
            problem(f"{label}: {spec_id} carries another specification's number")
        define_identifier(label, spec_id)
        covers = AC_TOKEN_RE.findall(cells[2])
        if not covers:
            note(f"{label}: {spec_id} names no acceptance criterion in 'Covers'")
        for criterion in covers:
            if criterion not in covered_criteria.get(label, set()):
                problem(f"{label}: {spec_id} covers {criterion}, which this "
                        "specification does not define as an acceptance criterion")
        if cells[4].lower() not in TASK_STATUSES:
            note(f"{label}: {spec_id} status {cells[4]!r} is outside "
                 f"{', '.join(TASK_STATUSES)}")
    if rows == 0 and required_now:
        problem(f"{label}: tasks.adoc carries no task rows while the status is {status}")


# Acceptance criteria defined per specification, filled by ``check_spec``
# before ``check_plan_and_tasks`` reads it for the task rows.
covered_criteria: dict[str, set[str]] = {}


def check_spec(spec_dir: Path) -> None:
    """Everything that is checked about one specification directory."""
    label = spec_dir.name
    match = SPEC_DIR_RE.fullmatch(label)
    if match is None:  # unreachable: check_tree filters on the same pattern
        return
    number = match.group(1)
    if number == "000":
        problem(f"{label}: specification numbering starts at 001")

    spec_path = spec_dir / "spec.adoc"
    if not spec_path.is_file():
        problem(f"{label}: spec.adoc is missing")
        return
    text = spec_path.read_text(encoding="utf-8")

    attrs = attributes(text)
    status = attrs.get("status", "").split()[0] if attrs.get("status", "").split() else ""
    if not status:
        problem(f"{label}: ':status:' is missing from the header")
    elif status not in STATUSES:
        problem(f"{label}: unknown status {status!r} "
                f"(one of {', '.join(STATUSES)})")
    enforced = status in ENFORCED_STATUSES

    title = TITLE_RE.search(text)
    if title is None:
        problem(f"{label}: the title line '= Spec NNN: <title>' is missing")
        return
    if title.group(1) == "NNN":
        (problem if enforced else note)(
            f"{label}: the title still reads 'Spec NNN' — name the specification")
    elif title.group(1) != number:
        problem(f"{label}: the title says Spec {title.group(1)}, "
                f"the directory says {number}")

    if unfilled(title.group(2)):
        (problem if enforced else note)(
            f"{label}: the title still carries a template placeholder")
    check_header(label, attrs, status)
    check_sections(label, text)

    if enforced and "NEEDS CLARIFICATION" in text:
        problem(f"{label}: 'NEEDS CLARIFICATION' remains while the status is {status}")

    requirements = check_requirements(label, text, number)
    covered = check_criteria(label, text, number, requirements, enforced)
    covered_criteria[label] = set(
        f"AC-{match.group(1)}-{match.group(2)}" for match in CRITERION_RE.finditer(text))

    withdrawn = {spec_id for spec_id, line in requirements.items()
                 if "withdrawn" in line.lower()}
    uncovered = sorted(spec_id for spec_id in requirements
                       if spec_id not in covered and spec_id not in withdrawn)
    if uncovered:
        message = (f"{label}: requirement(s) with no acceptance criterion: "
                   f"{', '.join(uncovered)}")
        (problem if enforced else note)(message)

    check_plan_and_tasks(label, spec_dir, number, status)


def attributes(text: str) -> dict[str, str]:
    """The document-header attributes; the last occurrence wins."""
    found: dict[str, str] = {}
    for match in ATTR_RE.finditer(text):
        found[match.group(1)] = match.group(2)
    return found


def check_tree(root: Path) -> None:
    """Walk the specifications: directories, templates, then each spec."""
    entries = sorted(path for path in root.iterdir() if path.is_dir())
    specs = [path for path in entries if SPEC_DIR_RE.fullmatch(path.name)]
    for path in entries:
        if path.name != "_templates" and path not in specs:
            problem(f"{path.name}: the directory name must read NNN-<slug> "
                    "(three digits, a hyphen, a lowercase slug)")
    for template in TEMPLATES:
        if not (root / "_templates" / template).is_file():
            note(f"_templates/{template} is missing — the process templates are "
                 "referenced by conventions/process.md")
    if not specs:
        note("no specifications yet — the directory is valid while empty")
    numbers = []
    for path in specs:
        match = SPEC_DIR_RE.fullmatch(path.name)
        if match is not None:
            numbers.append(int(match.group(1)))
    numbers.sort()
    for current, following in zip(numbers, numbers[1:]):
        if following != current + 1:
            note(f"specification numbers skip from {current:03d} to {following:03d}")
    for spec_dir in specs:
        check_spec(spec_dir)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("specs_dir", nargs="?", default=str(SPECS_DIR),
                        help="the specifications (default: docs/specs)")
    args = parser.parse_args()

    root = Path(args.specs_dir)
    if not root.is_dir():
        print(f"spec_check: specifications directory not found: {root}")
        return 2

    check_tree(root)

    for message in notes:
        print(f"spec_check: note: {message}")
    for message in problems:
        print(f"spec_check: PROBLEM: {message}")
    print(f"spec_check: {'PASS' if not problems else 'CHECK'} — "
          f"{len(problems)} problem(s), {len(notes)} note(s)")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
