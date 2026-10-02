"""doit task definitions for FASTENgine.

The repository's task runner: `doit` drives the context-tree gates, the Bazel
build, the test suite and the documentation build, so a developer and CI run
the same commands.

Usage:
    doit                 # verify + build + test (the CI set)
    doit list            # every task, one line each
    doit verify          # the verification gates (context tree + specifications)
    doit build           # bazel build //...
    doit test            # bazel test //...
    doit format          # clang-format -i over the engine sources
    doit format_check    # clang-format --dry-run --Werror (writes nothing)
    doit docs            # build the documentation (arc42 + ADRs + API reference + architecture pages)
    doit docs_check      # check the documentation tree (see docs/development/conventions/docs.md)
    doit diagrams        # render docs/arc42/diagrams/*.puml into docs/arc42/images/
    doit spec_check      # validate the specifications (docs/specs)
    doit trace           # traceability report (acceptance criteria ↔ tests) into build/trace/

Exit codes: doit exits 0 when every requested task succeeds, 1 otherwise.
"""

import os
import shutil
import subprocess
from pathlib import Path

DOIT_CONFIG = {
    "default_tasks": ["verify", "build", "test"],
    "verbosity": 2,
}

GATE_DIR = Path(".agents/skills/verify-rules/scripts")
SOURCE_SUFFIXES = (".hpp", ".cpp")
DOCS_BUILD_DIR = Path("build/docs")


def _engine_sources():
    """Every C++ source under `src/` — the files the formatting rules bind."""
    return sorted(
        str(path)
        for path in Path("src").rglob("*")
        if path.is_file() and path.suffix in SOURCE_SUFFIXES
    )


def _has_bazel_targets():
    """True once any package declares targets — the state this stub reports on.

    `bazel build //...` fails in a workspace without a single BUILD file, so the
    tasks below say what is missing instead of failing on an empty repository.
    """
    for dirpath, dirnames, filenames in os.walk("."):
        dirnames[:] = [d for d in dirnames if d != ".git" and not d.startswith("bazel-")]
        if "BUILD.bazel" in filenames or "BUILD" in filenames:
            return True
    return False


def task_verify():
    """Run the verification gates: snippets compile, links, anchors and layout resolve; the specifications validate."""
    return {
        "actions": [
            ["python3", str(GATE_DIR / "verify_rule_docs.py"), ".agents", "docs/development",
             "--group", "block", "--compiler", "clang++", "--std", "c++17"],
            ["python3", str(GATE_DIR / "check_heading_numbering.py"),
             "docs/development/conventions/style/naming.md",
             "-r", "docs/development/conventions"],
            ["python3", str(GATE_DIR / "check_context_layout.py"),
             "--root", ".agents", "--repo", "."],
            ["python3", "tools/spec_check.py", "docs/specs"],
        ],
    }


def task_spec_check():
    """Validate the specifications (`docs/specs`): structure, identifiers, status, links."""
    return {"actions": [["python3", "tools/spec_check.py", "docs/specs"]]}


def task_build():
    """Build every Bazel target — nothing to build until the first BUILD file."""
    def build():
        if not _has_bazel_targets():
            print("no Bazel targets yet: the first BUILD.bazel brings them; "
                  "resolving the module graph instead")
            return subprocess.call(["bazel", "mod", "deps"]) == 0
        return subprocess.call(["bazel", "build", "//..."]) == 0

    return {"actions": [build]}


def task_test():
    """Run every Bazel test target — nothing to run until the first BUILD file."""
    def run_tests():
        if not _has_bazel_targets():
            print("no Bazel targets yet: the first BUILD.bazel brings them")
            return True
        return subprocess.call(["bazel", "test", "//..."]) == 0

    return {"actions": [run_tests]}


def task_format():
    """Format the engine sources in place (clang-format, `.clang-format`)."""
    def run_format():
        sources = _engine_sources()
        if not sources:
            print("no engine sources yet")
            return True
        return subprocess.call(["clang-format", "-i", *sources]) == 0

    return {"actions": [run_format]}


def task_format_check():
    """Check the engine sources without writing (clang-format --dry-run --Werror)."""
    def run_check():
        sources = _engine_sources()
        if not sources:
            print("no engine sources yet")
            return True
        return subprocess.call(["clang-format", "--dry-run", "--Werror", *sources]) == 0

    return {"actions": [run_check]}


def task_docs_check():
    """Check the documentation tree: ADR set, generated regions, includes, links."""
    return {"actions": [["python3", "tools/check_docs.py"]]}


def task_trace():
    """Write the traceability report (acceptance criteria ↔ tests) into build/trace/."""
    return {"actions": [["python3", "tools/trace.py"]]}


def task_diagrams():
    """Render the PlantUML diagram sources into docs/arc42/images/ (SVG)."""
    return {"actions": [["python3", "tools/render_diagrams.py"]]}


def task_docs():
    """Build the documentation: arc42 + ADRs to HTML, the architecture pages, and the API site."""
    def build_docs():
        for tool in ("asciidoctor", "pandoc", "doxygen"):
            if shutil.which(tool) is None:
                print(f"no '{tool}' on PATH — see docs/development/toolchain.md")
                return False

        arc42_dir = DOCS_BUILD_DIR / "arc42"
        adr_dir = arc42_dir / "adr"
        adr_dir.mkdir(parents=True, exist_ok=True)
        (DOCS_BUILD_DIR / "api").mkdir(parents=True, exist_ok=True)

        if subprocess.call(["python3", "tools/render_diagrams.py"]) != 0:
            return False
        if subprocess.call(["python3", "tools/check_docs.py"]) != 0:
            return False

        # asciidoctor recovers from some parse errors with exit 0 — an
        # `asciidoctor: ERROR` line still fails the build here.
        proc = subprocess.run(["asciidoctor", "-b", "html5",
                               "-o", str(arc42_dir / "arc42.html"),
                               "docs/arc42/arc42.adoc"],
                              capture_output=True, text=True)
        if proc.stderr.strip():
            print(proc.stderr.strip())
        if proc.returncode != 0 or "asciidoctor: ERROR" in proc.stderr:
            return False

        adrs = sorted(str(path) for path in Path("docs/arc42/adr").glob("[0-9]*.adoc"))
        if adrs:
            proc = subprocess.run(["asciidoctor", "-b", "html5", "-D", str(adr_dir), *adrs],
                                  capture_output=True, text=True)
            if proc.stderr.strip():
                print(proc.stderr.strip())
            if proc.returncode != 0 or "asciidoctor: ERROR" in proc.stderr:
                return False

        images = Path("docs/arc42/images")
        if images.is_dir():
            shutil.copytree(images, arc42_dir / "images", dirs_exist_ok=True)

        if subprocess.call(["python3", "tools/render_arc42_pages.py"]) != 0:
            return False

        if subprocess.call(["doxygen", "docs/api/Doxyfile"]) != 0:
            return False

        print(f"documentation built into {DOCS_BUILD_DIR}/")
        return True

    return {"actions": [build_docs]}
