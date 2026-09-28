# Hook: format on edit

Automation **specification** — intent, not a harness config: the real form (a shell hook, a settings file, an editor action) is generated per harness by an adapter (see [`../adapters/README.md`](../adapters/README.md)).

**Status**: half-realized — `.clang-format` exists and reproduces the examples of `style/documentation.md` (4 spaces, Allman, 100 columns), so the action below is ready to run: `doit format` writes, `doit format_check` checks. What is missing is the automatic trigger; until an editor or a harness fires it, the task is run by hand.

```
on:     file-edit
match:  src/**/*.{hpp,cpp}
action: clang-format -i $FILE
mode:   advisory
```
