# Eval: naming compliance of new code

**Status**: stub — the criteria are mechanical and the tooling exists today (Bazel + doit, GoogleTest); the scenario's difficulty is not yet calibrated against a real round.

## Scenario

A fresh session starts in this repository with `AGENTS.md` and the development conventions (`docs/development/conventions/**`) available, and is asked: *"Add `ring_buffer.hpp` and `ring_buffer.cpp`: a fixed-capacity byte ring buffer for a single producer and a single consumer."* Nothing else is said — the rules must carry the naming.

## Expected behavior

The agent reads the naming rules before writing, then produces: the `@file` block, the type with its prefix and role, members with access markers and correct marker blocks, imperative-verb method names, `this->` on non-`static` method calls with fields accessed bare, and Doxygen coverage matching the table in `style/documentation.md`.

## Pass criteria (mechanical)

- `doit build` exits 0, and `doit test` exits 0 with the new test target passing, on both front ends (`bazel test //...` and `bazel test //... --config=gcc16`); C++17 and `-Wall -Wextra -Wpedantic` come from `.bazelrc`.
- Every member declaration in the class body carries an access marker; no member function does.
- No `this->` on a field; no unqualified call to a `static` member function.
- Documentation coverage: every entity of the mandatory table in `style/documentation.md` carries its block, and no `@throw`/`@exception` appears (the project forbids exceptions).

## Known false negatives

The criteria read names and coverage, not intent: a semantically wrong but conventionally named buffer passes. Pair this eval with a review by the `naming-auditor` persona when the semantic side matters.
