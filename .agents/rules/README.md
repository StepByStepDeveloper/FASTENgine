# Rules

**Status**: placeholder — the layer is a declared seam: it holds no rule yet, and it opens only when a file passes the admission test below.

Standing rules that bind the agent's work in this repository and belong to no other layer. Nothing attaches a rule to a path automatically, so a file here is visible only through the [`AGENTS.md`](../../AGENTS.md) router table and the links below.

## What the neighbouring layers already own

| Kind of norm | Home |
|:--|:--|
| Conventions with a human reader (style, naming, git, testing, docs) | [`docs/development/conventions/`](../../docs/development/conventions/README.md) — canonical; `.agents/` links, never copies |
| Prohibitions, and the paths never to read | [`../policies/guardrails.md`](../policies/guardrails.md), [`../ignore`](../ignore) |
| A procedure for a recurring task | [`../skills/`](../skills) |
| A ready prompt invoked by name | [`../commands/`](../commands) |
| Facts that outlive a session | [`../state/memory.md`](../state/memory.md) |
| Anything a gate, hook, linter or formatter can enforce | the mechanism itself — a check that can refuse outranks a sentence that asks |

## Admission test

A file may live here only if **all** of the following hold:

1. **Standing** — it binds every unit of work in this repository, not one task (a task-shaped procedure is a skill).
2. **Agent-only** — no human reader needs it; a norm with a developer audience lives in the development manual, and this tree links it.
3. **Not a prohibition** — "never …" statements are guardrails.
4. **Not mechanically enforceable** — what a gate, hook, linter or formatter can enforce is enforced there, not by prose.
5. **Earned** — written after the agent repeated a real mistake, never from a hypothetical preference; rules accrete from observed failures.

## Opening the layer

When the first rule passes the test: add its file (one topic per file, imperative), link it from the `AGENTS.md` router table, and update the layout check — which today admits this placeholder only — in the same change.
