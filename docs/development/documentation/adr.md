# Architecture decisions

Every decision with alternatives and lasting consequences is recorded as an ADR (Architecture Decision Record) in `docs/arc42/adr/`, one decision per file, and summarized in the index of Section 9 of the [arc42 document](arc42.md). The binding rules are the [Documentation System](../conventions/docs.md).

## When a decision needs an ADR

- A choice between alternatives with lasting consequences: toolchain, structure, protocol, an expensive-to-change API.
- An accepted decision changes: the old record is superseded, not rewritten.
- Not for: bug fixes, refactors that restore intended behaviour, or choices whose consequences fit in one commit's message.

## Creating one

```bash
python3 tools/new_adr.py "Short title of the decision" [--status accepted]
```

The generator numbers the file `NNNN-slug.adoc`, fills the template and rewrites both generated regions of Section 9. Never copy `adr-template.adoc` by hand, and never rename or renumber an ADR file.

## The shape

- Title line `= ADR-NNNN: <Title>`; anchor `[[adr-NNNN]]`; the Status line `Status: <status> (<YYYY-MM-DD>).` directly under it.
- Statuses: `proposed`, `accepted`, `rejected`, `deprecated`, `superseded by ADR-NNNN`.
- Sections: Context and Problem Statement, Decision Drivers, Considered Options, Decision Outcome (with Consequences), Confirmation, More Information. The shipped examples are ADR-0001, ADR-0002 and ADR-0003.

## Immutability

An accepted ADR's substance is immutable: typos may be fixed; a changed decision becomes a new ADR and the old record's status flips to `superseded by ADR-NNNN`. The history of *why* is the point.

## Pitfalls

- The marker regions of Section 9 are generated — write them only through the generator; `doit docs_check` fails when they drift from the files on disk.
- After a hand-edit of a title or a status line, run `python3 tools/new_adr.py --regenerate`.
- Code that realizes a decision names `ADR-NNNN` in its documentation block.

## Verification

`doit docs_check` reports PASS and the new record appears as a numbered subsection of Section 9 in the built document.
