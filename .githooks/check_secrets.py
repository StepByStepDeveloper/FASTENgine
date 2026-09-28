#!/usr/bin/env python3
"""Scan the staged content of a git repository for credential-shaped strings.

Enforces the policy of `.agents/policies/guardrails.md` — no credential, token,
private key or `.env` value is written into this repository — at the moment it
matters: the commit. The scan reads the staged (index) content, so it sees
exactly what the commit would record; changes that only live in the working
tree are out of scope.

It checks, per staged file:
  content   one finding per line that matches a credential shape: provider
            token prefixes, PEM blocks, JWTs, non-empty URL userinfo and
            credential-named `name = value` assignments whose value is not a
            placeholder
  names     staged paths that name secret-bearing files (`.env`, PEM blocks,
            SSH keys, credential stores) — the placeholder forms of `.env` are
            exempt

The check is heuristic: a match is evidence, not proof, and a credential whose
shape is not recognized is not caught. A line carrying the marker
`allowlist-secret` is exempt — deliberately rarely; give a reason next to it.
A finding names the file, the line and the rule, never the matched text, so a
report is safe to paste into an issue.

Usage:
    python3 check_secrets.py [--repo REPO]

Exit codes: 0 = clean, 1 = at least one finding (the commit should stop),
2 = the repository could not be inspected (not a git work tree).

Standard library only.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import subprocess
import sys

# A staged line carrying this marker is exempt from the content scan.
ALLOW_MARKER = "allowlist-secret"

# Staged basenames that must not exist in a commit (fnmatch, case-insensitive).
FILE_PATTERNS = (
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "*.p12",
    "*.pfx",
    "*.jks",
    "*.keystore",
    "*.kdbx",
    "*.ppk",
    "id_rsa*",
    "id_ed25519*",
    "id_ecdsa*",
    "id_dsa*",
    ".npmrc",
    ".netrc",
    ".pypirc",
    ".git-credentials",
    "credentials",
    "credentials.json",
)

# The placeholder forms of a `.env` file: examples, not values.
FILE_EXEMPT = (".env.example", ".env.sample", ".env.template", ".env.dist")

# Credential shapes, matched per line of staged content. Each rule is a shape,
# not a word list: a match is evidence, not proof. Rules are deliberately kept
# small enough to audit in a diff; a missed shape is a bug to add here.
PATTERNS = (
    # PEM blocks: private keys and other "-----BEGIN X-----" armor.
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    # GitHub: classic (ghp_/gho_/ghu_/ghs_/ghr_) and fine-grained (github_pat_) tokens.
    ("github-token", re.compile(r"\bgh[opusr]_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{22,}\b")),
    # AWS access key IDs (the secret key itself has no stable shape).
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    # OpenAI-style keys, both legacy and project-scoped.
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    # Stripe-style keys.
    ("stripe-key", re.compile(r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{16,}\b")),
    # Google API keys.
    ("google-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    # Slack tokens.
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    # JSON Web Tokens: three base64url segments, the first decoding to "{".
    ("jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")),
    # Telegram bot tokens.
    ("telegram-token", re.compile(r"\b\d{8,10}:AA[A-Za-z0-9_-]{30,}\b")),
    # Discord webhook URLs.
    ("discord-webhook", re.compile(r"https://(?:ptb\.|canary\.)?discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9_-]+")),
    # Hugging Face, GitLab, PyPI and npm tokens.
    ("huggingface-token", re.compile(r"\bhf_[A-Za-z0-9]{30,}\b")),
    ("gitlab-token", re.compile(r"\bglpat-[A-Za-z0-9_-]{20,}\b")),
    ("pypi-token", re.compile(r"\bpypi-[A-Za-z0-9_-]{50,}\b")),
    ("npm-token", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b")),
    # HTTP `Authorization: Bearer` style headers.
    ("bearer-token", re.compile(r"(?i)\bbearer[ \t]+[A-Za-z0-9._~+/-]{24,}=*")),
    # Non-empty userinfo with a password of 8+ characters in a URL.
    ("url-credentials", re.compile(r"[a-z][a-z0-9+.-]*://[^/\s:@]{1,64}:[^/\s:@]{8,}@")),
    # Assignments to credential-named variables; the value filter below keeps
    # placeholder-looking examples writable.
    ("credential-assignment", re.compile(r"(?i)\b(?:password|passwd|passphrase|secret|token|api[_-]?key|auth[_-]?key|access[_-]?key|client[_-]?secret)\b\s*[:=]\s*[\"']?([A-Za-z0-9_\-+=./]{16,})")),
)

# Values that read as placeholders rather than credentials.
PLACEHOLDER_WORDS = frozenset(
    {"changeme", "placeholder", "example", "dummy", "sample", "fake", "redacted", "none", "null", "empty"}
)
PLACEHOLDER_PREFIXES = ("your", "change", "xxxx", "example", "dummy", "sample", "placeholder", "fake", "redacted")


def _git(repo: str, *args: str) -> bytes:
    """Run one git command in `repo`; exit 2 if git cannot answer."""
    result = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", "replace").strip()
        print(f"check_secrets: git {' '.join(args)} failed: {detail}", file=sys.stderr)
        raise SystemExit(2)
    return result.stdout


def _staged_index(top: str) -> dict[str, str]:
    """Return ``{path: blob sha}`` for the regular files the commit would record."""
    index: dict[str, str] = {}
    for entry in _git(top, "ls-files", "-s", "-z").split(b"\0"):
        if not entry:
            continue
        meta, _, path = entry.partition(b"\t")
        fields = meta.split()
        if len(fields) == 3 and fields[2] == b"0" and fields[0].startswith(b"100"):
            index[path.decode("utf-8", "replace")] = fields[1].decode("ascii")
    return index


def _file_finding(name: str) -> bool:
    """True when a staged basename names a secret-bearing file."""
    lowered = name.lower()
    if lowered in FILE_EXEMPT:
        return False
    return any(fnmatch.fnmatch(lowered, pattern) for pattern in FILE_PATTERNS)


def _looks_placeholder(value: str) -> bool:
    """True for a value that reads as an example rather than a credential."""
    lowered = value.lower()
    return lowered in PLACEHOLDER_WORDS or lowered.startswith(PLACEHOLDER_PREFIXES)


def _assignment_is_credential(value: str) -> bool:
    """The assignment rule fires only for value-shaped, non-placeholder text."""
    if _looks_placeholder(value):
        return False
    classes = (
        any(c.islower() for c in value)
        + any(c.isupper() for c in value)
        + any(c.isdigit() for c in value)
        + any(not c.isalnum() for c in value)
    )
    return classes >= 2


def _content_findings(data: bytes) -> list[tuple[int, str]]:
    """Scan one staged blob; return ``[(line number, rule name)]``."""
    if b"\x00" in data[:8000]:
        return []  # binary content is not text to leak
    findings: list[tuple[int, str]] = []
    for lineno, line in enumerate(data.decode("utf-8", "replace").splitlines(), 1):
        if ALLOW_MARKER in line:
            continue
        for name, pattern in PATTERNS:
            match = pattern.search(line)
            if not match:
                continue
            if name == "credential-assignment" and not _assignment_is_credential(match.group(1)):
                continue
            findings.append((lineno, name))
            break
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scan the staged content of a repository for credential-shaped strings."
    )
    parser.add_argument("--repo", default=".", help="repository to inspect (default: the current directory)")
    args = parser.parse_args()

    top = _git(args.repo, "rev-parse", "--show-toplevel").decode("utf-8", "replace").strip()
    staged = [
        path
        for path in _git(top, "diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR")
        .decode("utf-8", "replace")
        .split("\0")
        if path
    ]
    if not staged:
        print("result: PASS (no staged changes)")
        return 0

    index = _staged_index(top)
    findings: list[tuple[str, str, str]] = []  # (path, location, rule)
    for path in staged:
        if _file_finding(os.path.basename(path)):
            findings.append((path, "", "forbidden-file-name"))
        sha = index.get(path)
        if sha is None:
            continue  # a deletion or a non-regular entry: nothing to read
        for lineno, rule in _content_findings(_git(top, "cat-file", "blob", sha)):
            findings.append((path, str(lineno), rule))

    for path, location, rule in findings:
        where = f"{path}:{location}" if location else path
        print(f"secret [{where}]: {rule}")
    if findings:
        files = len({path for path, _, _ in findings})
        print(
            f"result: FAIL ({len(findings)} finding(s) in {files} staged file(s)) — "
            f'the commit is blocked; fix the line, or add an "{ALLOW_MARKER}" marker with a reason'
        )
        return 1
    print(f"result: PASS ({len(staged)} staged file(s) scanned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
