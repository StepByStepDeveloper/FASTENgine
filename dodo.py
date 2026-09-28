"""doit task definitions for FASTENgine.

The repository's task runner: `doit` drives the context-tree gates, the Bazel
build and the test suite, so a developer and CI run the same commands.

Usage:
    doit                 # verify + build + test (the CI set)
    doit list            # every task, one line each
    doit verify          # context-tree gates only
    doit build           # bazel build //...
    doit test            # bazel test //...
    doit format          # clang-format -i over the engine sources
    doit format_check    # clang-format --dry-run --Werror (writes nothing)

Exit codes: doit exits 0 when every requested task succeeds, 1 otherwise.
"""

import os
import subprocess
from pathlib import Path

DOIT_CONFIG = {
    "default_tasks": ["verify", "build", "test"],
    "verbosity": 2,
}

GATE_DIR = Path(".agents/skills/verify-rules/scripts")
SOURCE_SUFFIXES = (".hpp", ".cpp")


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
    """Run the context-tree gates: snippets compile, links, anchors and layout resolve."""
    return {
        "actions": [
            ["python3", str(GATE_DIR / "verify_rule_docs.py"), ".agents",
             "--group", "block", "--compiler", "clang++", "--std", "c++17"],
            ["python3", str(GATE_DIR / "check_heading_numbering.py"),
             ".agents/rules/style/naming.md", "-r", ".agents/rules"],
            ["python3", str(GATE_DIR / "check_context_layout.py"),
             "--root", ".agents", "--repo", "."],
        ],
    }


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
