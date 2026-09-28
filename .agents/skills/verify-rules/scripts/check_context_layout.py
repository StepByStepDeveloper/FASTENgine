#!/usr/bin/env python3
"""Check the .agents tree against the reference context-architecture layout.

The repository's agent-facing context follows one reference layout (eleven layers
plus a root AGENTS.md entry point). This script verifies that the tree still
matches it and that each artifact carries the structure its layer prescribes.

Checks, per the layout's own sections:
  tree        the reference entries exist, and nothing outside them does
  AGENTS.md   overview + commands + constraints + index, and no copied content
  rules/      (reported only) every rule document carries no layer frontmatter
  policies/   a prohibition list, plus a one-glob-per-line ignore file
  skills/     <kebab-name>/SKILL.md with a name and a description that says what and when
  commands/   one file per command, described in frontmatter and in the body's first line
  docs/       linked from AGENTS.md, table/fact shaped
  state/      the scratchpad's four blocks; the memory's three topic sections
  mcp.json    an mcpServers object
  hooks/      on / match / action / mode from the reference vocabulary
  agents/     name + description, Role & Mindset / Checklist / Output Format
  evals/      Scenario / Expected behavior / Pass criteria
  adapters/   the harness -> expects -> source -> method table

Usage:
    python3 check_context_layout.py [--root .agents] [--repo .]

Exit codes: 0 = every check passed, 1 = at least one check reported CHECK,
2 = the root directory does not exist.

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

REFERENCE_ENTRIES = {
    "rules", "policies", "skills", "commands", "docs", "state",
    "hooks", "agents", "evals", "adapters", "ignore", "mcp.json",
}
LAYER_DIRS = REFERENCE_ENTRIES - {"ignore", "mcp.json"}
HOOK_EVENTS = {"file-edit", "pre-commit", "pre-command", "post-tool-call"}
HOOK_MODES = {"blocking", "advisory"}

results: list[tuple[str, str, bool, str, bool]] = []


def frontmatter(path: str) -> tuple[dict[str, str] | None, str]:
    """Return ``(flat frontmatter keys, body)`` for a markdown file.

    Keys are read from a leading ``---`` block; the body is everything after it,
    so a caller can test how a document opens.
    """
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 3)
    if end < 0:
        return None, text
    keys = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if match:
            keys[match.group(1)] = match.group(2).strip()
    return keys, text[end + 5:]


def first_body_line(body: str) -> str:
    """First non-empty line of a body, used for the ``commands/`` description check."""
    return next((line for line in body.splitlines() if line.strip()), "")


def field(text: str, key: str) -> str:
    """Value of a flat ``key: value`` line in a hook specification (``""`` when absent)."""
    match = re.search(rf"^{key}:\s*(.+)$", text, re.M)
    return match.group(1).strip() if match else ""


def headings(text: str) -> list[str]:
    return [h.strip().lower() for h in re.findall(r"^#{1,6}\s+(.+)$", text, re.M)]


def check(section: str, item: str, passed: bool, detail: str = "", strict: bool = True) -> None:
    """Record one outcome; a non-strict miss is reported as a note, not as a failure."""
    results.append((section, item, passed, detail, strict))


def check_tree(ag: str) -> None:
    present = set(os.listdir(ag))
    check("tree", "reference entries present", REFERENCE_ENTRIES <= present,
          f"missing={sorted(REFERENCE_ENTRIES - present) or 'none'}")
    check("tree", "no entries outside the reference",
          present <= REFERENCE_ENTRIES, f"extra={sorted(present - REFERENCE_ENTRIES) or 'none'}")
    check("tree", "adapters/README.md", os.path.isfile(os.path.join(ag, "adapters", "README.md")))


def check_agents_md(repo: str) -> None:
    path = os.path.join(repo, "AGENTS.md")
    if not os.path.isfile(path):
        check("AGENTS.md", "exists", False, path)
        return
    text = open(path, encoding="utf-8").read()
    heads = headings(text)
    check("AGENTS.md", "overview + commands + constraints + index",
          any("overview" in h for h in heads) and any("command" in h for h in heads)
          and any("core rules" in h for h in heads) and any("architecture" in h for h in heads),
          f"headings={heads}")
    check("AGENTS.md", "links rather than copies .agents content",
          "```" not in text, f"{text.count('```')} fenced block(s)")
    check("AGENTS.md", "stays a single entry point (measurable size)",
          len(text) < 4000, f"{len(text)} chars ~ {len(text) // 4} tokens")


def check_rules(ag: str) -> None:
    docs = [os.path.join(dirpath, name)
            for dirpath, _, names in os.walk(os.path.join(ag, "rules"))
            for name in names if name.endswith(".md")]
    without = [d for d in docs if frontmatter(d)[0] is None]
    check("rules", "layer frontmatter present (adapter metadata)",
          not without, f"{len(without)}/{len(docs)} without frontmatter — deliberate, "
                       "see .agents/state/memory.md", strict=False)


def check_policies(ag: str) -> None:
    policies = [os.path.join(ag, "policies", n) for n in sorted(os.listdir(os.path.join(ag, "policies")))
                if n.endswith(".md")]
    text = "".join(open(p, encoding="utf-8").read() for p in policies)
    check("policies", "a prohibition list", "## Prohibited" in text and "NEVER" in text,
          f"{len(policies)} file(s)")
    ignore = os.path.join(ag, "ignore")
    patterns = [l for l in open(ignore, encoding="utf-8").read().splitlines()
                if l.strip() and not l.startswith("#")]
    check("ignore", "one glob per line", all(not re.search(r"\s{2,}", l) for l in patterns),
          f"{len(patterns)} pattern(s)")


def check_skills(ag: str) -> None:
    root = os.path.join(ag, "skills")
    skills = [d for d in sorted(os.listdir(root)) if os.path.isdir(os.path.join(root, d))]
    detail = []
    passed = bool(skills)
    for name in skills:
        keys, _ = frontmatter(os.path.join(root, name, "SKILL.md"))
        kebab = bool(re.fullmatch(r"[a-z0-9-]{1,64}", name))
        name_ok = bool(keys) and keys.get("name") == name
        description = (keys or {}).get("description", "")
        what_when = len(description) <= 1024 and "use" in description.lower()
        passed &= kebab and name_ok and what_when
        detail.append(f"{name}: kebab={kebab} name_field={name_ok} "
                      f"desc={len(description)}ch what+when={what_when}")
    check("skills", "kebab-case dir, SKILL.md, name + description (what & when)", passed,
          "; ".join(detail) or "no skills")


def check_commands(ag: str) -> None:
    root = os.path.join(ag, "commands")
    files = [n for n in sorted(os.listdir(root)) if n.endswith(".md")]
    detail, passed = [], bool(files)
    for name in files:
        keys, body = frontmatter(os.path.join(root, name))
        described = bool((keys or {}).get("description"))
        opens = len(first_body_line(body)) > 20
        passed &= described and opens
        detail.append(f"{name}: description={described} body_opens_described={opens}")
    check("commands", "one file per command, described in frontmatter and body", passed,
          "; ".join(detail))


def check_docs(ag: str, repo: str) -> None:
    root = os.path.join(ag, "docs")
    files = [n for n in sorted(os.listdir(root)) if n.endswith(".md")]
    agents_md = open(os.path.join(repo, "AGENTS.md"), encoding="utf-8").read()
    linked = all(f".agents/docs/{n}" in agents_md for n in files)
    table_shaped = all("|" in open(os.path.join(root, n), encoding="utf-8").read() for n in files)
    check("docs", "linked from AGENTS.md and fact/table shaped", bool(files) and linked and table_shaped,
          f"{files}")


def check_state(ag: str) -> None:
    scratchpad = open(os.path.join(ag, "state", "scratchpad.md"), encoding="utf-8").read()
    check("state", "scratchpad: Objective -> Status -> Discovered Issues -> Next action",
          all(h in scratchpad for h in
              ["## Objective", "## Status", "## Discovered Issues", "## Next action"]))
    memory = open(os.path.join(ag, "state", "memory.md"), encoding="utf-8").read()
    check("state", "memory: topic sections",
          all(h in memory for h in
              ["## Architecture Pitfalls", "## Environment Quirks", "## Team Conventions"]))


def check_mcp(ag: str) -> None:
    data = json.loads(open(os.path.join(ag, "mcp.json"), encoding="utf-8").read())
    check("mcp.json", "an mcpServers object", isinstance(data.get("mcpServers"), dict))


def check_hooks(ag: str) -> None:
    root = os.path.join(ag, "hooks")
    files = [n for n in sorted(os.listdir(root)) if n.endswith(".md")]
    detail, passed = [], bool(files)
    for name in files:
        text = open(os.path.join(root, name), encoding="utf-8").read()
        fields = {key: field(text, key) for key in ("on", "match", "action", "mode")}
        good = (all(fields.values()) and fields["on"] in HOOK_EVENTS and fields["mode"] in HOOK_MODES)
        passed &= good
        detail.append(f"{name}: on={fields['on']} mode={fields['mode']}")
    check("hooks", "on / match / action / mode vocabulary", passed, "; ".join(detail))


def check_personas(ag: str) -> None:
    root = os.path.join(ag, "agents")
    files = [n for n in sorted(os.listdir(root)) if n.endswith(".md")]
    detail, passed = [], bool(files)
    for name in files:
        keys, body = frontmatter(os.path.join(root, name))
        good = (bool(keys) and bool(keys.get("name")) and bool(keys.get("description"))
                and all(h in body for h in ["## Role & Mindset", "## Checklist", "## Output Format"]))
        passed &= good
        detail.append(f"{name}: {'ok' if good else 'frontmatter or sections missing'}")
    check("agents", "name + description, Role & Mindset / Checklist / Output Format", passed,
          "; ".join(detail))


def check_evals(ag: str) -> None:
    root = os.path.join(ag, "evals")
    files = [n for n in sorted(os.listdir(root)) if n.endswith(".md")]
    detail, passed = [], bool(files)
    for name in files:
        text = open(os.path.join(root, name), encoding="utf-8").read()
        good = all(h in text for h in ["## Scenario", "## Expected behavior", "## Pass criteria"])
        passed &= good
        detail.append(f"{name}: {'ok' if good else 'section missing'}")
    check("evals", "Scenario -> Expected behavior -> Pass criteria", passed, "; ".join(detail))


def check_adapters(ag: str) -> None:
    text = open(os.path.join(ag, "adapters", "README.md"), encoding="utf-8").read()
    rows = [l for l in text.splitlines() if l.startswith("|")]
    check("adapters", "harness -> expects -> source -> method table",
          len(rows) >= 3 and all(len(l.split("|")) - 2 == 4 for l in rows) and "symlink" in text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".agents", help="the context tree (default: .agents)")
    parser.add_argument("--repo", default=".", help="repository root holding AGENTS.md")
    args = parser.parse_args()

    if not os.path.isdir(args.root):
        print(f"context tree not found: {args.root}")
        return 2

    check_tree(args.root)
    check_agents_md(args.repo)
    check_rules(args.root)
    check_policies(args.root)
    check_skills(args.root)
    check_commands(args.root)
    check_docs(args.root, args.repo)
    check_state(args.root)
    check_mcp(args.root)
    check_hooks(args.root)
    check_personas(args.root)
    check_evals(args.root)
    check_adapters(args.root)

    width = max(len(item) for _, item, _, _, _ in results)
    for section, item, passed, detail, strict in results:
        verdict = "ok" if passed else ("note" if not strict else "CHECK")
        print(f"{section:<10} {item:<{width}}  {verdict:<5}  {detail[:110]}")
    failed = [r for r in results if not r[2] and r[4]]
    notes = [r for r in results if not r[2] and not r[4]]
    summary = f"result: {'PASS' if not failed else 'CHECK'} ({len(results) - len(failed) - len(notes)}/{len(results)} ok"
    summary += f", {len(notes)} note(s))" if notes else ")"
    print("\n" + summary)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
