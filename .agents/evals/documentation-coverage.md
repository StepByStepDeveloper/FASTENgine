# Eval: documentation coverage of new code

**Status**: stub — the criteria are mechanical and the tooling exists today (Bazel + doit, a `Doxyfile`); the scenario's difficulty is not yet calibrated against a real round.

## Scenario

A fresh session starts in this repository with `AGENTS.md` and `.agents/rules/**` available, and is asked: *"Add `ring_buffer.hpp` and `ring_buffer.cpp`: a fixed-capacity byte ring buffer for a single producer and a single consumer."* The naming rules carry the names; this eval reads the comments.

## Expected behavior

The agent documents every entity of the mandatory-coverage table before reporting: the `@file` block, the type block with `@details` and `@invariant`, one comment per enumerator, `@param`/`@return`/`@pre` on the functions, blocks on the data members, and `@note`/`@warning` where the contract carries a hazard. Error paths are described through the return channel, never as exceptions.

## Pass criteria (mechanical)

- Every entity of the table in `style/documentation.md` carries its block — check the new files entity by entity.
- No `@throw` / `@exception` / `@throws` in the new files.
- No placeholder block (`/** */`), no `// TODO: document`.
- `doxygen Doxyfile` reports no undocumented-entity warning for the new files.
- `doit build` and `doit test` exit 0.

## Known false negatives

The criteria read presence and shape, not truth: a comment that is present but wrong passes every one of them. Clause-level correctness is the `documentation-auditor` persona's job.
