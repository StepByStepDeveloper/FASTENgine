# Hook: format on edit

Automation **specification** — intent, not a harness config: the real form (a shell hook, a settings file, an editor action) is generated per harness by an adapter (see [`../adapters/README.md`](../adapters/README.md)).

**Status**: not realized. `clang-format` is installed (see [`../docs/toolchain.md`](../docs/toolchain.md)), but no `.clang-format` file exists in the repository root, so the tool would fall back to LLVM style — which is **not** what [`../rules/style/formatting.md`](../rules/style/formatting.md) prescribes (4 spaces, Allman, 100-120 characters). Write the config file first, then flip the mode.

```
on:     file-edit
match:  src/**/*.{hpp,cpp}
action: clang-format -i $FILE
mode:   advisory
```
