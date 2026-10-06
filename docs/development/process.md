# The development process

This chapter is the guided tour of how a change happens in FASTENgine: the path from an idea to merged, verified code, walked end to end on one small feature — and through the two halves of a feature's life that may be far apart in time: planning (the package is written and agreed) and implementation (the package becomes code). The binding rules live in [Process (SDD + ADR + TDD)](conventions/process.md); this chapter shows them in action, in the order you meet them. Read it once before your first feature, then come back to the step you are on. If you just need to get the repository building, start with [Getting started](getting-started.md) and return here when you pick up a real feature.

## Why a process at all

The process here is deliberately small: four documents and one loop. It exists because features here are built by developers — with AI agents as an optional accelerator — and the failure modes of moving fast are known:

- code written faster than it is understood — the *why* evaporates;
- tests written after the code — they verify what is, not what should be;
- decisions argued twice, because the first argument left no record;
- a task — given to a person or to an agent — without a contract, so the gaps get filled with invention.

The four documents are the contract (a **specification**), the record (**ADRs**), the plan (`plan.adoc`) and the work breakdown (`tasks.adoc`); the loop is **red-green-refactor**. Everything below is those five things, applied to one feature — and every step is a command or a document: the process runs identically with no agent in the room. The agent-side artifacts (`.agents/`) only mirror the steps — see [Working with agents](working-with-agents.md).

## The example: a byte ring buffer

To keep the walkthrough honest, we will follow one real-shaped feature — a fixed-capacity byte ring buffer, the kind of leaf the engine's type layer will start from — as if it were specification 001. Nothing else in this chapter is specific to ring buffers. At the end, this is what the repository will contain because of one feature:

```
docs/specs/001-byte-ring-buffer/spec.adoc      — status: Implemented
docs/specs/001-byte-ring-buffer/plan.adoc
docs/specs/001-byte-ring-buffer/tasks.adoc
docs/arc42/adr/0008-byte-ring-buffer-spsc-only.adoc   — accepted
src/types/ring_buffer.hpp  src/types/ring_buffer.cpp
src/types/ring_buffer_test.cpp  src/types/BUILD.bazel
build/trace/report.md                          — no uncovered criteria
```

## 1. Specify

A specification starts life as a copy of the templates:

```bash
cp -r docs/specs/_templates docs/specs/001-byte-ring-buffer
```

Then you fill `spec.adoc` top to bottom. The writing guide is [Specifications](documentation/specs.md); here is what each section means in practice.

**Goal** — why this exists and for whom, three to five sentences. If you cannot write it without "and also", you have two features:

```
== Goal

The engine needs a staging buffer that carries bytes between a producer thread
and a consumer thread without allocating and without a lock. This feature
provides a fixed-capacity byte ring buffer with a single-producer,
single-consumer contract: the producer calls push, the consumer calls pop, and
neither call allocates after construction.
```

**Context and Non-goals** — what it touches, and what a reader might expect but will not get. Non-goals are the cheapest place to prevent scope creep:

```
== Non-goals

* Multiple producers or multiple consumers — the contract fails loudly in review, not at runtime.
* A blocking mode — a waiting pop is a different feature with a scheduler behind it.
```

**Requirements** — functional requirements in EARS form, one per line, numbered. EARS is a fill-in-the-blank grammar that keeps statements testable; the five patterns:

| Pattern | Template | Example (this feature) |
|:--|:--|:--|
| Ubiquitous | The `<system>` shall `<response>` | The buffer shall not allocate after construction. |
| Event-driven | When `<trigger>`, the `<system>` shall `<response>` | When `push` is called with free capacity, the buffer shall store the byte. |
| State-driven | While `<state>`, the `<system>` shall `<response>` | While the buffer is full, `push` shall reject the byte and change nothing. |
| Unwanted behavior | If `<condition>`, then the `<system>` shall `<response>` | If `pop` is called on an empty buffer, then no state shall change. |
| Optional feature | Where `<feature>`, the `<system>` shall `<response>` | Where the debug poison mode is enabled, the buffer shall overwrite vacated slots with a fixed pattern. |

Non-functional requirements must be measurable, with the conditions and the configuration they are measured on:

```
=== Non-functional

* NFR-001-01: On the reference configuration (x86-64, GCC 16, -O2), push and pop
  shall be wait-free for their respective threads.
* NFR-001-02: sizeof(C_RingBuffer) shall not exceed 64 bytes plus the storage.
```

**Acceptance criteria** — one per line, checkable by a test, naming the requirement it discharges. State the observable result, not the implementation:

```
== Acceptance Criteria

* AC-001-01 (FR-001-01): Given an empty buffer of capacity 4, when push(0xAB) runs,
  then it returns true, the size is 1, and pop() returns 0xAB.
* AC-001-02 (FR-001-02): Given a full buffer, when push(0xCD) runs, then it returns
  false and the size is unchanged.
* AC-001-03 (FR-001-03): Given an empty buffer, when pop() runs, then it returns
  nothing and the size stays zero.
* AC-001-04 (FR-001-04): Given a capacity of zero, when the buffer is constructed,
  then the request is rejected — a precondition violation, asserted in debug builds.
* AC-001-05 (NFR-001-01): Given the TSan concurrency test, when the producer and
  the consumer run, then TSan reports no data races.
```

**Open questions** — every open point is spelled `NEEDS CLARIFICATION` in place; that marker is what gates approval. Everything else in the file is written as if it were already true.

Run the checker whenever you like — it is patient while the status is `Draft`:

```bash
doit spec_check
```

```
spec_check: PASS — 0 problem(s), 2 note(s)
```

The “shape of green”: while the status is `Draft`, missing sections and template placeholders are notes; the moment the status is `Approved`, the same findings become problems. Nothing in the file can be forgotten silently — it is either written or it is red.

## 2. Decide

Somewhere in the specification there is usually a decision hiding: a choice with alternatives and lasting consequences. Here it is obvious — the buffer is single-producer/single-consumer, and the rejected alternative (general thread-safety, a lock) has consequences for everything that will call it. That choice gets an **ADR**, before the package goes to the review:

```bash
python3 tools/new_adr.py "Byte ring buffer is single-producer/single-consumer"
```

The generator assigns the next free number (call it `ADR-0008`), fills the template and updates the index in arc42 §9. The record is short: Context, Drivers, Options, Outcome, Consequences. An accepted ADR is immutable in substance — when the decision changes later, it is superseded, never rewritten. The full shape is in [Decision records](documentation/adr.md); who writes and who accepts is in [Process](conventions/process.md).

The `:adr:` attribute in the specification header now names `ADR-0008`, so the spec and the decision point at each other.

## 3. Plan

`plan.adoc` answers *how*: the approach, the affected arc42 building blocks, the public API sketch, the data and concurrency model, the test strategy. It is part of the planning package — written before the review, and reviewed together with the ADRs it references — and it is where the contract becomes signatures:

```C++
#include <cstddef>
#include <cstdint>
#include <optional>

/**
 * @brief Fixed-capacity byte ring buffer for a single producer and a single consumer.
 * @details Backing storage is allocated once; after construction the buffer never
 *          allocates, and each operation is wait-free for its own side (see ADR-0008).
 * @invariant The stored byte count never exceeds the capacity passed to the constructor.
 */
class C_RingBuffer
{
public:
    /// @brief Creates a buffer with the given capacity in bytes; the capacity must be greater than zero.
    explicit C_RingBuffer(std::size_t capacity) noexcept;

    /// @brief Stores one byte; returns false when the buffer is full and nothing was written.
    bool push(std::uint8_t byte) noexcept;

    /// @brief Removes and returns the oldest byte; an empty optional means the buffer was empty.
    std::optional<std::uint8_t> pop() noexcept;

    /// @brief Returns the number of bytes currently stored.
    std::size_t retrieveSize() const noexcept;
};
```

The plan also names its test strategy — here: unit tests for the state machine, one concurrency test under ThreadSanitizer — and its risks. If the plan surfaces a decision it cannot settle, that decision goes back through step 2 as an ADR; it does not get buried in prose.

## 4. Slice into tasks

`tasks.adoc` is the work breakdown: one row, one behavior, one test. The “Covers” column ties every task to an acceptance criterion, and the Bazel target names where its test will live:

```
[cols="1,4,2,2,2"]
|===
| ID | Description | Covers | Bazel target | Status

| T-001-01 | Construction rejects zero capacity | AC-001-04 | //src/types:ring_buffer_test | done
| T-001-02 | Push then pop returns the byte; size follows | AC-001-01 | //src/types:ring_buffer_test | todo
| T-001-03 | Push on a full buffer fails and changes nothing | AC-001-02 | //src/types:ring_buffer_test | todo
| T-001-04 | Pop on an empty buffer returns nothing | AC-001-03 | //src/types:ring_buffer_test | todo
| T-001-05 | Concurrent producer/consumer smoke, TSan clean | AC-001-05 | //src/types:ring_buffer_concurrency_test | todo
|===
```

The tasks are sliced *before* the review — feature planning reads them to place the work. The package is now complete: the specification, the decisions, the plan, the tasks; the next step agrees it.

## 5. Agree at the review

Approval is the moment the specification stops being prose and becomes a promise: requirements settled, criteria checkable, decisions accepted, no `NEEDS CLARIFICATION` left. It happens at the **architectural review and feature planning** — one event or two, and a whole batch of packages can cross it together:

- the **architectural review** half reads the package as architecture: criteria a test can embody, ADRs that settle the decisions, contracts that hold together;
- the **feature planning** half places it: priority, the team that will implement, and when.

Only the owner approves — the author drafts, and never moves a specification across this line itself.

```
:status: Approved
```

The next `doit spec_check` is no longer patient: from here on, an incomplete section, an empty acceptance criterion, an open question — or a missing plan or task list — is a failure, not a note. That is the point — the draft relaxed, the promise does not.

An *Approved* specification waits as the agreed backlog: implementation may start right away or much later, by its authors or by another team. Deferring is normal, not an exception — that is how planning runs ahead of implementation.

## 6. Implement: the TDD cycle

The implementation phase begins when a team picks the package up — possibly long after the review; before the first task, walk the [Definition of Ready](conventions/process.md) once more and confirm the package is still current. Every task walks the same three-step loop; task T-001-02 shown in full. The test comes first, and it fails for the right reason — a behavioral expectation, not a missing symbol.

**Red.** Write the test; show the failure. The test carries its specification anchor, so the report and `doit trace` can see it:

```
/// @file ring_buffer_test.cpp
/// @brief Behavior tests for C_RingBuffer.

#include "ring_buffer.hpp"

#include <gtest/gtest.h>

/**
 * @brief Verifies that a byte pushed into an empty buffer comes back out of pop.
 * @covers{AC-001-01}
 */
TEST(RingBuffer, PushThenPopReturnsTheByte)
{
    C_RingBuffer buffer{4};

    ASSERT_TRUE(buffer.push(0xAB));
    EXPECT_EQ(buffer.retrieveSize(), 1U);

    const std::optional<std::uint8_t> byte = buffer.pop();
    ASSERT_TRUE(byte.has_value());
    EXPECT_EQ(byte.value(), 0xAB);
    EXPECT_EQ(buffer.retrieveSize(), 0U);
}
```

```bash
bazel test //src/types:ring_buffer_test
```

```
--- FAIL: Expected equality of these values: buffer.retrieveSize() (0) == 1U
```

**Green.** The smallest change that makes the test pass — and nothing else. Run the test again; it passes. No other test may break: the suite is run whole at this point, not per target.

**Refactor.** With everything green, improve the structure — a named constant, a clearer name, a deduplicated branch — and re-run the suite. Then mark the task `done` in `tasks.adoc` and move to the next row. The tasks file is the status board; nothing else tracks the work.

Two rules keep the loop honest, and both are load-bearing:

- **Tests are never weakened to reach green.** If an existing test fails, either the change is wrong or the test encodes a contract that is genuinely changing — and that is the owner's decision, not a detail to be smoothed over.
- **One task, one behavior, one test.** A task that needs the word “and” is two tasks.

For the concurrency task, the cycle is the same with the tools turned up: the smoke test runs repeatedly, and the target is exercised under ThreadSanitizer (`--config=tsan` once the sanitizer configurations exist in the build); a race that TSan reports is a red step, not an acceptable flake. The mechanics of the test framework and the quality bar are in [Testing](conventions/testing.md).

## 7. Close the feature

The feature is not done when the last test passes — it is done when the checklist in [Process](conventions/process.md) holds. In this repository that means, in order:

1. **Traceability.** `doit trace` must be clean: every acceptance criterion of the specification covered by at least one test, and no `@covers` naming an identifier that does not exist.

   ```bash
   doit trace
   ```

   ```
   trace: PASS — report: build/trace/report.md (0 problem(s), 0 note(s))
   ```

2. **The full gate.** `doit verify`, `doit build`, `doit test` — and for anything the feature documents, `doit docs`. A red gate stops the change; you fix the artifact, never the gate.
3. **The specification.** Status to `Implemented`; anything that turned out different was already updated in the same commits (see step 8).
4. **The architecture.** New building block joins arc42 §5 and `docs/api/groups.dox` in the same change; the concurrency model joins §8; the ADR reference joins §9 (the generator maintains the index).
5. **The pull request.** The template asks the questions the process cares about — specification, criteria covered, gates run, red-step evidence. A PR body that cannot answer them is the earliest signal that a step was skipped.

## 8. Live on

A specification is a contract of intent, not a historical record. When reality disagrees with it — a criterion was unobservable, a requirement was wrong, a decision changed — the specification changes in the same commit as the code, so the difference stays visible in the diff. A change of wording is just an edit; a change of a recorded decision goes through a new ADR that supersedes the old one. A specification that is replaced wholesale is marked `Superseded` and stays on disk: its identifiers are permanent addresses and are never recycled.

Periodically — at releases, and at the quarterly review named in the process conventions — the specifications in *Implementing* are walked for stalled features, and the risks and debt they accumulated land in arc42 §11.

## Where to next

- [Working with agents](working-with-agents.md) — the same steps with an optional agent at your side.
- [Process (SDD + ADR + TDD)](conventions/process.md) — the binding rules this chapter demonstrated.
- [Specifications](documentation/specs.md) — the writing guide and the checklists for a specification, a plan and a task list.
- [Decision records](documentation/adr.md) — how an ADR is created, accepted and superseded.
- [Glossary](glossary.md) — every term and abbreviation this manual uses, in one place.
