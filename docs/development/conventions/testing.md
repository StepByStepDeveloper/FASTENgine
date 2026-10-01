# Testing Strategy

## Overview

Ensuring stability and correctness through automated testing in FASTENgine.

## Frameworks

- **Primary Framework**: GoogleTest — every test is a Bazel `cc_test` target next to the code it covers.
- **Mocking**: GoogleMock. Both arrive through the `googletest` Bazel module (one target family since 1.18.0: `@googletest//:gtest` carries the test and mock libraries, `@googletest//:gtest_main` provides `main()`).

## Testing Principles

- **Unit Tests**: Test individual components in isolation. Use mocks for external dependencies.
- **Integration Tests**: Test the interaction between major modules (e.g., Renderer + Window System).
- **Regression Testing**: Ensure new changes do not break existing functionality.

## Test-Driven Development

Implementation is written test-first; the binding process is [Process](process.md). The loop: specification criterion -> failing test -> minimal code -> refactor.

- **Red first, for the right reason**: add an API stub so the test compiles and fails on the unfulfilled expectation, not on a missing symbol; the failing output belongs in the report or the PR.
- **One test, one behavior**: Arrange-Act-Assert; the name states the behavior, `@brief` the expected outcome.
- **Traceability**: a test that verifies a specification criterion carries `@covers{AC-NNN-ii}`; implementation names its requirement with `@implements{FR-NNN-ii}` where the link is not obvious from its group — see [Process](process.md).
- **Existing tests change only with the developer's explicit approval**; weakening a test to make a change pass hides a defect — the opposite of a finished task.
- **State-based assertions**; mock only at the boundary to the outside world.
- **Concurrency code** runs repeatedly and under ThreadSanitizer; **performance requirements** are verified by benchmarks with documented conditions.

## Requirements

- **Coverage is a consequence, not a target**: every acceptance criterion has at least one test (`doit trace`); a high number without traceability means little.
- **Documentation**: test code is production code — every test case and test helper carries detailed Doxygen comments (see [Documentation](style/documentation.md)).
- **Deterministic Tests**: Tests must be deterministic and not depend on system time or external state unless controlled.
- **Speed**: Unit tests should be extremely fast.

## Running Tests

```bash
doit test                                  # bazel test //... — every target
bazel test //src/types:ring_buffer_test    # one target
doit trace                                 # the traceability report (criteria ↔ tests)
```

A test source is code like any other: it follows the naming rules, and its `@brief` names the behavior under test and the expected outcome (see [Documentation](style/documentation.md)).
