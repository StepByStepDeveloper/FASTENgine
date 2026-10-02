# Glossary

The terms and abbreviations used across this manual and in the process artifacts. Where a term has a home document, it is linked; the definitions here are one-liners by design, not a second copy of the rules.

| Term | Full form | What it means here |
|:--|:--|:--|
| AC | Acceptance Criterion | A checkable statement that says when a requirement is met; written `AC-NNN-ii`, covered by tests, counted by `doit trace`. |
| ADR | Architecture Decision Record | One decision, its alternatives and its consequences, in one immutable file under `docs/arc42/adr/` — see [Decision records](documentation/adr.md). |
| Agent | — | An AI collaborator working in this repository: drafts specifications and ADRs, writes tests and code, never approves its own work. |
| arc42 | — | The fixed twelve-section architecture document template this repository uses under `docs/arc42/`. |
| ASan | Address Sanitizer | Runtime checker for memory errors; one of the sanitizer configurations of the build. |
| Author | — | Whoever drives a feature: writes the specification, walks the statuses, implements under TDD. |
| Bazel | — | The build system; targets are addressed as `//path:name`. |
| Bazelisk | — | The launcher that reads `.bazelversion` and runs the pinned Bazel — the only supported way to call Bazel here. |
| BUILD file | — | `BUILD.bazel`: the file declaring a directory's Bazel targets. |
| `cc_test` | — | The Bazel rule for a C++ test target; every test in this repository is one. |
| Context tree | — | `.agents/` and `docs/development/` together — the pair the `doit verify` gates guard. |
| DoD | Definition of Done | The checklist that closes a feature — see [Process](conventions/process.md). |
| DoR | Definition of Ready | The checklist that lets implementation start — see [Process](conventions/process.md). |
| `doit` | — | The task runner (`dodo.py`); `doit list` names every task this repository defines. |
| Doxygen | — | The tool that builds the API reference from the comment blocks in the code — see [Documentation (Doxygen)](conventions/style/documentation.md). |
| EARS | Easy Approach to Requirements Syntax | The five-pattern grammar for requirement statements used in specifications — see [Process](conventions/process.md). |
| Feature | — | One capability, described by exactly one specification and its artifacts. |
| FR / NFR | Functional / Non-Functional Requirement | Numbered requirement forms `FR-NNN-ii` / `NFR-NNN-ii` inside a specification. |
| Gate | — | A mechanical check that must pass: `doit verify`, `doit spec_check`, `doit trace`, `doit docs_check`, the build and the test suite. |
| GoogleMock / GoogleTest | — | The unit-test and mocking frameworks; every test is a `cc_test` target. |
| Gherkin-style | — | The Given/when/then phrasing used by acceptance criteria. |
| `NEEDS CLARIFICATION` | — | The literal marker for an open point in a specification; approval is blocked while one remains. |
| Owner | — | The human authority in the loop: approves specifications, accepts ADRs, approves changes to existing tests. |
| Plan | — | `plan.adoc`: how the feature will be built — approach, contracts, test strategy. |
| PlantUML | — | The diagram source format under `docs/arc42/diagrams/`; renders are built by `doit diagrams`. |
| Red / Green / Refactor | — | The three steps of the TDD cycle: a failing test, the smallest change that passes it, then structure under green. |
| SDD | Specification-Driven Development | The method: the specification is written and approved before implementation, and stays the contract of intent afterward. |
| Spec | Specification | `spec.adoc`: what is being built and how it will be verified — see [Specifications](documentation/specs.md). |
| Specifications (the) | — | The `docs/specs/` tree: one directory per feature (`spec.adoc`, `plan.adoc`, `tasks.adoc`) plus the templates; validated by `doit spec_check`. |
| Spike | — | A time-boxed experiment that answers one feasibility question; thrown away when the answer is in. |
| Status | — | A specification's lifecycle position: `Draft -> Approved -> Implementing -> Implemented`, or `Superseded`. |
| T | Task | A work item `T-NNN-ii` in `tasks.adoc`: one behavior, one test, one passing commit. |
| TDD | Test-Driven Development | The implementation loop: tests before code, red before green — see [Testing](conventions/testing.md). |
| Traceability | — | The link chain specification -> test -> code, carried by `@covers{AC-NNN-ii}` and `@implements{FR-NNN-ii}` and verified by `doit trace`. |
| TSan | Thread Sanitizer | Runtime checker for data races; one of the sanitizer configurations of the build. |
| UBSan | Undefined Behavior Sanitizer | Runtime checker for undefined behavior; one of the sanitizer configurations of the build. |
