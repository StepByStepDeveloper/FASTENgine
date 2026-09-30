---
name: write-adr
description: "Record an architecture decision as an ADR — create, fill, supersede. Use when a non-trivial decision with alternatives is settled or revisited."
---

# Record an ADR

How a FASTENgine decision becomes an immutable record in `docs/arc42/adr/` and a row in Section 9's index. Conventions: [docs.md](../../../docs/development/conventions/docs.md); the shipped examples are ADR-0001 through ADR-0003.

**Status**: active — the generator, the template and the checks exist.

## When to Use

- A choice between alternatives with lasting consequences is made: toolchain, structure, protocol, an API that is expensive to change.
- An accepted decision changes: the old record is superseded, not rewritten.
- Don't use for: bug fixes, refactors that restore intended behaviour, or choices whose consequences fit in one commit's message.

## Procedure

1. **Create the file through the generator:**
   ```bash
   python3 tools/new_adr.py "Short title of the decision" [--status accepted]
   ```
   It numbers the file `NNNN-slug.adoc`, fills the template and rewrites Section 9's generated regions. Never copy `adr-template.adoc` by hand.
2. **Fill every section** — Context and Problem Statement, Decision Drivers, Considered Options, Decision Outcome (with Consequences), Confirmation, More Information. Keep it short: options *considered*, not a survey; consequences honest, the bad ones included.
3. **Set the Status line** (fixed form `Status: <status> (<YYYY-MM-DD>).` under the title): `proposed`, `accepted`, `rejected`, `deprecated` or `superseded by ADR-NNNN`. Update the line when the state changes — the record below it stays.
4. **Supersede, never rewrite.** A changed decision is a new ADR plus `superseded by ADR-NNNN` in the old record's status. Fixing a typo is allowed; changing the substance is not.
5. **Point at it from code and architecture.** The realizing entities name `ADR-NNNN` in their documentation block; the ADR's *More Information* links the affected building blocks and files.
6. **Verify:** `python3 tools/check_docs.py` exits 0.

## Pitfalls

- Renaming or renumbering the file by hand breaks the anchor, the title and the index at once. After editing a title or status line by hand, run `python3 tools/new_adr.py --regenerate`; never touch the marker regions yourself.
- The date in the Status line is the state's date, not the file's creation date — the generator reads it back into the index.
- One decision per file. If the title needs "and", it is probably two ADRs.

## Verification

`doit docs_check` reports PASS and the new ADR appears as its own numbered subsection of Section 9 in `build/docs/arc42/arc42.html`.
