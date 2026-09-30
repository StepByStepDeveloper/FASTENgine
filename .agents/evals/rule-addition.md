# Eval: adding a rule consistently

**Status**: stub — the criteria are runnable today (the gate exists); the scenario's difficulty is not yet calibrated against a real round.

## Scenario

*"Add a rule about `<topic>` to the development conventions (`docs/development/conventions`)"* — a convention that belongs to an existing document rather than opening a new one.

## Expected behavior

The convention lands in the document that owns it, in every home it needs; the report names what passed, what stays open, and which home was deliberately omitted and why; the diff is left uncommitted.

## Pass criteria (mechanical)

- The convention appears in all five homes — table row, normative notice, the exception section it names, a compiled example, and that example's "this example covers" list — or the report names the home it deliberately omits and why.
- `verify_rule_docs.py --group block` exits 0 on `clang++`, `g++` and `g++-16` at `--std c++17`.
- `check_heading_numbering.py` exits 0 on every numbered document, anchors included.
- Retired wording does not survive the change: grep the tree for the vocabulary the rule replaced.
- The diff is left uncommitted, and the report states what passed and what stays open.

## Known false negatives

The criteria do not read the new rule's *content* — a well-wired but false statement passes every one of them. Clause-level correctness is the `rule-doc-reviewer` persona's job, and an eval for it needs a case whose right answer is settled by a compiled probe.
