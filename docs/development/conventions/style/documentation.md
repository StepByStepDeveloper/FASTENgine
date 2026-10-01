# Documentation (Doxygen)

Every piece of code created in FASTENgine **must** be accompanied by detailed Doxygen comments. Documentation is a first-class deliverable: an undocumented (or misdocumented) entity is a review blocker, exactly like a missing test or a violated naming rule.

This document defines *what* must be documented, *which* commands to use, and *what counts as detailed*. The tooling (Doxyfile, generation target, CI gate) is intentionally not covered here — it lives in [Documentation System](../docs.md).

## Comment form

- **Command prefix**: always `@` (e.g. `@brief`), never the `\` form. Mixing the two within one file is forbidden.
- **Block form** — a `/** ... */` block is mandatory for any entity whose contract does not fit on a single line. It is placed on its own lines immediately above the declaration, at the same indentation level, with **no blank line** between the block and the declaration.
- **Single-line form** — `/// @brief ...` on its own line above the declaration, or the trailing form `///< @brief ...` on the same line after a member/enumerator, is allowed only for entities whose whole contract is one short clause.
- **Language**: English only (see the `Language` core rule in `AGENTS.md`).
- **Formatting**: comment text obeys the `Formatting` rules — 4-space indentation, max 100-120 characters, no tabs. Continuation lines of a block align with the block's first `*`.
- **Where the documentation lives**: the full contract block is written on the **declaration** (header). The matching definition in a `.cpp` file carries no Doxygen block — only ordinary `//` implementation comments — so that the same entity is not documented twice. Entities with no declaration in a header (internal helpers, anonymous-namespace functions, `static` file-local variables) are documented at their definition.

## Fixed command order

Within one block, commands appear in this order, so that every block in the codebase reads the same way:

1. `@brief` (mandatory, always first)
2. `@details` — extended description, the *how* and the *why*
3. `@tparam` — one per template parameter, in declaration order
4. `@param` — one per function parameter, in declaration order
5. `@return` / `@retval`
6. `@pre` / `@post` / `@invariant`
7. `@note` / `@warning`
8. `@see` / `@ref` / `@deprecated`
9. `@code{.cpp}` … `@endcode` — usage example
10. `@covers{...}` / `@implements{...}` — specification anchors (see *Cross-entity requirements*)
11. `@todo` — only for work already tracked in the repository's issue tracker

## Mandatory coverage

| Entity                                     | Required                                                                                       |
|:------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| `.hpp` / `.cpp` file                       | `@file` block with `@brief` (+ `@details` for non-obvious responsibilities)                    |
| Namespace (named and anonymous)            | `@brief`                                                                                       |
| `class` / `struct` / `union` type          | Block: `@brief`, `@details`; `@tparam` per template parameter; `@invariant` where applicable   |
| `enum` / `enum class` type                 | Block: `@brief`, plus one `///<` or block per enumerator (meaning of every value)              |
| Function / method (free, member, static)   | Block: `@brief`, `@details` (non-trivial), `@param` per parameter, `@return` unless `void`     |
| Constructor / destructor                   | Block: `@brief`, `@param` per parameter, stated invariants established / released              |
| Type alias (`using` / `typedef`)           | `/// @brief` stating what the alias resolves to and why it exists                              |
| Function-like macro                        | Block: `@brief`, `@param` per macro parameter, `@note` on evaluation/parenthesization hazards  |
| Object-like macro                          | `@brief` (units, valid range, how the value is derived)                                        |
| Variable: global / namespace-scope         | `///< @brief` or block — meaning, units, valid range, ownership, thread-safety                 |
| Variable: class data member (any access)   | Same as namespace-scope variables; required for `static`, `thread_local`, `mutable` members    |
| Variable: local (block scope)              | Not required — see `Exceptions`; required when it carries non-obvious semantics                |
| Template parameter (all six kinds)         | `@tparam` describing the contract imposed on the argument                                      |
| Test case (see `docs/development/conventions/testing.md`) | `@brief` naming the behavior under test and the expected outcome; `@covers{AC-NNN-ii}` when the test verifies a specification criterion |

## Required content by entity kind

### Files

Every header and source file opens with a file block:

```C++
/**
 * @file ring_buffer.hpp
 * @brief Fixed-capacity byte ring buffer for single-producer/single-consumer pipelines.
 * @details Backing storage is caller-provided; the class never allocates and never copies.
 *          All operations are lock-free and wait-free for a single producer and a single consumer.
 */
```

`@file` should name the artifact the way a reader expects to find it, and must state what the file owns rather than listing its contents.

### Namespaces

`@brief` states the responsibility of the namespace (a bounded topic, e.g. "frame rendering pipeline"), not a list of its members.

### Types

A type block answers: what does an instance *mean*, what invariants must hold, who owns the resource, and how does it relate to other types. For every template parameter, `@tparam` must state the requirement imposed on the argument — not merely repeat its name:

```C++
#include <cstddef>

/**
 * @brief Owns the vertex storage of one mesh and provides read access to it.
 * @details The mesh never copies vertex data: the constructor stores the caller's pointer and every
 *          accessor hands it back. Objects are movable; duplication is an explicit operation.
 * @tparam TTP_Vertex Vertex component type (in practice @c float or @c double) used for both position and normal data.
 * @invariant @c priv_vertices_p is non-null and @c priv_vertexCount is greater than zero.
 * @warning The object holds a view over the storage passed to the constructor; destroying that
 *          storage first leaves the mesh dangling.
 * @see C_MeshLoader
 */
template <typename TTP_Vertex>
class C_Mesh
{
public:
    /**
     * @brief Creates a mesh over a caller-provided vertex array.
     * @param[in,out] vertices_p Vertex array of at least @p vertexCount elements;
     *                           ownership stays with the caller and the storage must outlive this object.
     * @param[in] vertexCount Number of vertices in @p vertices_p; must be greater than zero.
     * @pre @p vertices_p != nullptr
     */
    C_Mesh(TTP_Vertex* vertices_p, std::size_t vertexCount)
        : priv_vertices_p(vertices_p), priv_vertexCount(vertexCount)
    {
    }

    /**
     * @brief Returns the number of vertices covered by this mesh.
     * @return Vertex count; never zero for a validly constructed mesh.
     */
    std::size_t retrieveVertexCount() const { return priv_vertexCount; }

private:
    /// @brief Vertex array owned by the caller; must outlive this object.
    TTP_Vertex* priv_vertices_p;

    /// @brief Number of vertices in @c priv_vertices_p; strictly greater than zero.
    std::size_t priv_vertexCount;
};
```

Role-marked types (see `style/naming.md`) document their contract accordingly: an `IC_`/`IS_` interface documents the obligations on implementations, an `AC_`/`AS_` abstract type documents its partial implementation, and a `PC_`/`PS_`/`PAC_`/`PAS_` protocol documents exactly what the derived type must provide, naming the contract member that requires it.

### Enumerators

Every enumerator is documented. `enum class` values get a trailing `///< @brief`; a value whose meaning needs more than one clause gets its own block instead:

```C++
/**
 * @brief Outcome of a non-blocking push into the ring buffer.
 */
enum class E_PushResult
{
    Ok,     ///< @brief The byte was written; the write cursor has advanced.
    Full,   ///< @brief The buffer holds no free space; nothing was written and no cursor moved.
    Closed  ///< @brief The buffer was closed by the consumer; further pushes are permanent no-ops.
};
```

`@brief` is always written explicitly — the short forms above are not allowed to fall back on a Doxygen auto-brief setting, so that the rules hold regardless of the generated configuration.

### Functions and methods

A function block must let a caller use the function **without reading its body**:

- `@brief` — one clause, semantics rather than a paraphrase of the identifier.
- `@details` — required for any function with side effects, hidden state, ordering requirements, complexity, or a non-obvious algorithm.
- `@param[in]` / `@param[out]` / `@param[in,out]` — **every** parameter, exactly once, in declaration order, each with the directional specifier. References (`_r` / `_rc` … per naming rules) written to by the callee are `@param[out]` or `@param[in,out]`, never bare `@param`; a parameter that is never read and never written does not belong in the signature.
- `@return` — required for every non-`void` function: the meaning of the returned value, its units and range.
- `@retval` — required when distinct returned values carry distinct meanings; use one `@retval` per meaningful value instead of a vague `@return`.
- `@pre` / `@post` — required for every precondition the callee does not enforce itself (non-null pointers, index ranges, locked mutexes, initialized subsystems) and for every postcondition a caller may rely on.
- `@note` — thread-safety, reentrancy, complexity, ownership transfer, units, and rationale for surprising choices.
- `@warning` — anything that can cause undefined behavior, data loss, or a dangling resource when used as described.

Error reporting is documented through the return channel, because the project forbids exceptions (see `style/patterns.md`): for a `std::optional`, `std::expected`, error-code out-parameter or sentinel result, state the success payload *and* every failure condition with its cause and the caller's recovery options. `@throw`, `@exception` and `@throws` must never appear.

### Variables and members

Documented meaning, not a translation of the name: units, valid range, ownership (for pointers/references — who owns the pointee, how long it must outlive the object, whether ownership is transferred), lifetime, aliasing, thread-safety for `static`, `thread_local` and `mutable` members, and the relation to other fields:

```C++
#include <cstddef>
#include <cstdint>

class C_Logger
{
public:
    /**
     * @brief Number of live @c C_Logger instances; incremented by the constructor and decremented by the destructor.
     * @note Class-level storage shared by every instance; not thread-safe by itself.
     */
    static std::uint32_t pub_instanceCount_s;

    /// @brief Returns the age of the oldest entry that has not been flushed yet.
    /// @return Age in milliseconds, saturated at the configured flush timeout; never decreasing.
    std::uint32_t retrieveLastFlushAge() const { return prot_lastFlushAge; }

protected:
    /// @brief Milliseconds since the last successful flush; saturated at the configured timeout.
    std::uint32_t prot_lastFlushAge;

private:
    /**
     * @brief One past the last written entry of the caller-provided sink; the sink must not be
     *        reallocated while the logger is alive.
     */
    std::byte* priv_sinkEnd_p;
};
```

`mutable` and access-marker rules are not repeated in documentation — the name already carries them (`style/naming.md`); the comment carries the *semantics*.

### Macros

Every macro carries a block. Function-like macros document each parameter, state that the expression evaluates its arguments exactly once (or exactly which of them are evaluated more than once), and warn about the missing parentheses/`do { } while (0)` hazards where relevant. A macro whose only purpose is to alias a constant is documented with `@brief` stating the value's meaning and, where applicable, its unit.

## Cross-entity requirements

- **Code words in prose**: a parameter is referenced as `@p name` (so that Doxygen links it), any other identifier, keyword or literal as `@c word`. Neither form is ever left as bare text.
- **Related entities** are linked with `@ref` / `@see` / `@sa` when a reader needs them to use the documented entity correctly.
- **Specification anchors**: a test that verifies a specification criterion states it as `@covers{AC-NNN-ii}`; an implementation entity that realizes a requirement states it as `@implements{FR-NNN-ii}` when the link is not obvious from its Doxygen group. The anchors are the machine-readable half of [Process](../process.md); `doit trace` reports every anchor that matches nothing.
- **Non-trivial public APIs** ship a short `@code{.cpp} … @endcode` usage example in the type or function block (compilable code, following every rule in `style/naming.md`).
- **Deprecations** are never silent: `@deprecated` plus the replacement entity and the reason.

## Exceptions

The following entities are **not** required to carry Doxygen comments:

- **Trivial locals** — loop indices, single-use temporaries, clearly named intermediate results. They are explained inline with `//` only when they are non-obvious (magic values, units, invariants, ownership of a raw pointer, an intentional lifetime extension).
- **Trivial accessors** — one-line getters/setters whose name fully expresses the semantics (e.g. `retrieveVehicleCount()`, `setVehicleCount()`). A restating comment on them is forbidden rather than encouraged.
- **Self-evident lambdas and local functors** passed directly to an algorithm.
- **Third-party, vendored and generated code** (e.g. `vcpkg_installed/`, generated bindings) — never documented and never reformatted; its comments are left exactly as upstream wrote them.
- **Illustrative code fragments inside `docs/development/conventions/**`** that exist to demonstrate a *different* convention (e.g. the `Ultimate compilable example` in `style/naming.md`) may omit Doxygen comments, provided the fragment states the omission. Fragments that illustrate this document are documented and follow every rule in this folder; they are kept compilable, and together they form a single translation unit that produces no compiler error. Such a fragment declares entities nothing reads, so a warning-enabled build reports them: Clang flags the unread private member of the members example above (`-Wunused-private-field`), while GCC stays silent on the same code.

- **Skill tooling scripts** (`.agents/skills/**/scripts/`) — helper scripts a skill invokes. They are written in Python and carry a module docstring stating their interface, usage and exit codes, plus function docstrings where the behavior is not obvious, in place of Doxygen blocks: nothing generates Doxygen output from that folder, and the interpreter and `--help` are what read them.
- **Repository tooling scripts** (`dodo.py`, `.githooks/*`, `tools/**`) — the task runner, the git hooks and any helper the repository keeps for itself. They carry the same kind of self-description in place of Doxygen blocks: a module docstring for Python stating what it does, how it is invoked and what it returns, and a header comment for a shell script stating the same. Nothing generates Doxygen output from them either; their reader is whoever runs them.

Nothing else is exempt. Materially non-trivial code is always documented, regardless of visibility: `private` members and internal helpers are read by maintainers at least as often as public API is read by callers.

## Prohibited

- **Missing documentation** — an undocumented entity is a blocker, not a follow-up. Never leave `// TODO: document` or an empty `/** */` block behind as a placeholder.
- **Restating the code** — `@brief Flushes the buffer.` on `flushBuffer()`, `@param value The value.`, `@return The result.` These add no information and hide the absence of real documentation.
- **Wrong or stale documentation** — a comment that contradicts the code is worse than no comment. Documentation is updated **in the same commit** as the behavior it describes; code changes are incomplete until their docs change with them.
- **Copied documentation** — a comment pasted from a neighbouring entity without adjusting it. `@copydoc` is allowed only when the inherited semantics are genuinely identical; an override that deviates documents its own behavior.
- **Metadata noise** — `@author`, `@date` and `@version` must not be used: authorship and change history are authoritative in git and must not be duplicated in comments.
- **Non-standard commands** — only the standard command set listed above plus the two specification anchors (`@covers`, `@implements`, defined as aliases in `docs/api/Doxyfile`) may be used; no `@threadsafety`-style or project-invented commands.
- **Commented-out code** — dead code is deleted, not annotated.

## Maintenance and verification

- A change that adds, removes or alters an entity updates its documentation as part of the same commit.
- Documentation is a **silent failure mode**: it is checked at self-review and at code review, and a missing/wrong/restating comment is rejected there. Reviewers may request a rewrite of a `@brief` that only paraphrases the identifier.
- Every C++ snippet in this folder is kept compilable and must obey every rule it illustrates; when a rule changes, the snippets that demonstrate it are re-checked against the compiler and updated in the same change.
