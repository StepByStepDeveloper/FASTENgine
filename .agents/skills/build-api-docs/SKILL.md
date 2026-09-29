---
name: build-api-docs
description: "Build the Doxygen API reference and keep it warning-free. Use when adding or changing Doxygen comments, module groups or the Doxyfile."
---

# Build the API Reference

The Doxygen half of the documentation: where the configuration lives, how the module tree maps onto Section 5 of the arc42 document, and how warnings are read as coverage checks. The writing rules: [documentation.md](../../rules/style/documentation.md); the system: [docs.md](../../rules/docs.md).

**Status**: active — the build runs today; it covers `docs/api/` while `src/` waits for its first sources.

## When to Use

- After adding or changing Doxygen comments, `docs/api/groups.dox` or `docs/api/Doxyfile`.
- When a new module or building block appears and must join the group tree.
- When the owner asks whether the API reference builds clean.

## Procedure

1. **Build** — `doit docs` (whole site), or alone, from the repository root:
   ```bash
   mkdir -p build/docs/api && doxygen docs/api/Doxyfile
   ```
   Doxygen resolves the paths in the Doxyfile against the directory it is started from — never run it from inside `docs/api/`.
2. **Read the warnings** (stderr). With `EXTRACT_ALL = NO` and `WARN_IF_UNDOCUMENTED = YES`, every warning is an entity missing its documentation block — fix it per the coverage table of [documentation.md](../../rules/style/documentation.md).
3. **Map modules.** Every level-1 or level-2 building block of Section 5 has one group in `docs/api/groups.dox`; members join it from their own documentation block. Add the group and the Section 5 entry in the same change.
4. **Take the output** — `build/docs/api/html/index.html` (generated; never committed).

## Pitfalls

- `WARN_AS_ERROR` is deliberately `NO` while `src/` is empty; the flip to `FAIL_ON_WARNINGS` is an open item in [docs.md](../../rules/docs.md). Do not flip it casually — and do not read the current state as a licence to leave warnings.
- A run with zero engine sources still proves the configuration: `groups.dox` and `mainpage.md` are processed without any `src/` file.
- `build/docs/api` is not created by doxygen itself: `mkdir -p` it (or let `doit docs` do it).

## Verification

`doxygen docs/api/Doxyfile` exits 0, stderr carries no `warning:` lines, and `build/docs/api/html/index.html` exists and lists the expected groups.
