# Eval: documentation maintenance alongside a code change

**Status**: stub — the criteria are mechanical and the tooling exists today (`doit docs_check`, `doit docs`); the scenario's difficulty is not yet calibrated against a real round.

## Scenario

A fresh session starts in this repository with `AGENTS.md` and `.agents/**` available, and is asked: *"Add the first engine module — `src/types/fixed_vector.hpp`, `src/types/fixed_vector.cpp` and the `BUILD.bazel` of `src/types`: a fixed-capacity vector for the pipeline stages."* The `documentation-coverage` eval reads the comments; this eval reads everything around them.

## Expected behavior

Before reporting, the session keeps the documentation system consistent: the new module joins its group in `docs/api/groups.dox`, and Section 5 of the arc42 document either records the building block or the session says explicitly why the section stays in template state. Any decision the module settles (the capacity and error model is a candidate) is recorded as an ADR through `python3 tools/new_adr.py` or flagged as an open question — never silently skipped. Generated territory (the Section 9 marker regions, `images/*.svg`) is never hand-edited.

## Pass criteria (mechanical)

- `doit docs_check` exits 0 and `doit docs` builds.
- `doxygen docs/api/Doxyfile` reports no undocumented-entity warning for the new files.
- The building block named in Section 5 (when recorded) and the group in `groups.dox` spell the same name.
- No hand edits between the generated markers of `sections/09_architecture_decisions.adoc` — `python3 tools/new_adr.py --regenerate` leaves the file unchanged.
- If an ADR was created: its file matches `NNNN-*.adoc`, its Status line parses, and the Section 9 regions list it.

## Known false negatives

The criteria read structure, not judgment: an ADR whose rationale is vacuous passes every one of them, as does a Section 5 entry that names a block without describing it. Content depth is the `documentation-auditor` persona's job.
