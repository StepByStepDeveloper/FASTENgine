# Naming Conventions

## Naming prefixes and their combinations

### Variable prefixes

- `c_`: `const/constexpr` variable (`c` - const)
- `s_`: `static` variable (`s` - static)
- `g_`: `global` scope variable (`g` - global)
- `n_`: `namespace` scope variable (`n` - namespace)
- `gc_`: `global` scope `const/constexpr` variable (`gc` - global const)
- `nc_`: `namespace` scope `const/constexpr` variable (`nc` - namespace const)
- `gs_`: `global` scope `static` variable (`gs` - global static)
- `ns_`: `namespace` scope `static` variable (`ns` - namespace static)
- `sc_`: `static` `const/constexpr` variable (`sc` - static const)
- `gsc_`: `global` scope `static` `const/constexpr` variable (`gsc` - global static const)
- `nsc_`: `namespace` scope `static` `const/constexpr` variable (`nsc` - namespace static const)

### Macro prefixes

- `macro_`: Object-like or function-like `macro`

### Enum prefixes

- `e_`: `enum` variable (`e` - enum)
- `ge_`: `global` scope `enum` variable (`ge` - global enum)
- `ne_`: `namespace` scope `enum` variable (`ne` - namespace enum)
- `ce_`: `const/constexpr` `enum` variable (`ce` - const enum)
- `gce_`: `global` scope `const/constexpr` enum variable (`gce` - global const enum)
- `nce_`: `namespace` scope `const/constexpr` enum variable (`nce` - namespace const enum)
- `se_`: `static` `enum` variable (`se` - static enum)
- `gse_`: `global` scope `static` `enum` variable (`gse` - global static enum)
- `nse_`: `namespace` scope `static` `enum` variable (`nse` - namespace static enum)
- `sce_`: `static` `const/constexpr` `enum` variable (`sce` - static const enum)
- `gsce_`: `global` scope `static` `const/constexpr` `enum` variable (`gsce` - global static const enum)
- `nsce_`: `namespace` scope `static` `const/constexpr` `enum` variable (`nsce` - namespace static const enum)

### Pointer prefixes

- `p_`: `pointer` (`p` - pointer)
- `gp_`: `global` scope `pointer` (`gp` - global pointer)
- `np_`: `namespace` scope `pointer` (`np` - namespace pointer)
- `pc_`: `pointer` to `const/constexpr` object (`pc` - pointer const)
- `gpc_`: `global` scope `pointer` to `const/constexpr` object (`gpc` - global pointer const)
- `npc_`: `namespace` scope `pointer` to `const/constexpr` object (`npc` - namespace pointer const)
- `cp_`: `const/constexpr` `pointer` (`cp` - const pointer)
- `gcp_`: `global` scope `const/constexpr` `pointer` (`gcp` - global const pointer)
- `ncp_`: `namespace` scope `const/constexpr` `pointer` (`ncp` - namespace const pointer)
- `cpc_`: `const/constexpr` `pointer` to `const/constexpr` object (`cpc` - const pointer const)
- `gcpc_`: `global` scope `const/constexpr` `pointer` to `const/constexpr` object (`gcpc` - global const pointer const)
- `ncpc_`: `namespace` scope `const/constexpr` `pointer` to `const/constexpr` object (`ncpc` - namespace const pointer const)
- `sp_`: `static` `pointer` (`sp` - static pointer)
- `gsp_`: `global` scope `static` `pointer` (`gsp` - global static pointer)
- `nsp_`: `namespace` scope `static` `pointer` (`nsp` - namespace static pointer)
- `spc_`: `static` `pointer` to `const/constexpr` object (`spc` - static pointer const)
- `gspc_`: `global` scope `static` `pointer` to `const/constexpr` object (`gspc` - global static pointer const)
- `nspc_`: `namespace` scope `static` `pointer` to `const/constexpr` object (`nspc` - namespace static pointer const)
- `scp_`: `static` `const/constexpr` `pointer` (`scp` - static const pointer)
- `gscp_`: `global` scope `static` `const/constexpr` `pointer` (`gscp` - global static const pointer)
- `nscp_`: `namespace` scope `static` `const/constexpr` `pointer` (`nscp` - namespace static const pointer)
- `scpc_`: `static` `const/constexpr` `pointer` to `const/constexpr` object (`scpc` - static const pointer const)
- `gscpc_`: `global` scope `static` `const/constexpr` `pointer` to `const/constexpr` object (`gscpc` - global static const pointer const)
- `nscpc_`: `namespace` scope `static` `const/constexpr` `pointer` to `const/constexpr` object (`nscpc` - namespace static const pointer const)

### Reference prefixes

- `r_`: `reference` (`r` - reference)
- `gr_`: `global` scope `reference` (`gr` - global reference)
- `nr_`: `namespace` scope `reference` (`nr` - namespace reference)
- `rc_`: `reference` to `const/constexpr` object (`rc` - reference const)
- `grc_`: `global` scope `reference` to `const/constexpr` object (`grc` - global reference const)
- `nrc_`: `namespace` scope `reference` to `const/constexpr` object (`nrc` - namespace reference const)
- `cr_`: `constexpr` `reference`, can only refer to an object that is usable in constant expressions (`cr` - constexpr reference)
- `gcr_`: `global` scope `constexpr` `reference`, can only refer to an object that is usable in constant expressions (`gcr` - global constexpr reference)
- `ncr_`: `namespace` scope `constexpr` `reference`, can only refer to an object that is usable in constant expressions (`ncr` - namespace constexpr reference)
- `sr_`: `static` `reference` (`sr` - static reference)
- `gsr_`: `global` scope `static` `reference` (`gsr` - global static reference)
- `nsr_`: `namespace` scope `static` `reference` (`nsr` - namespace static reference)
- `src_`: `static` `reference` to `const/constexpr` object (`src` - static reference const)
- `gsrc_`: `global` scope `static` `reference` to `const/constexpr` object (`gsrc` - global static reference const)
- `nsrc_`: `namespace` scope `static` `reference` to `const/constexpr` object (`nsrc` - namespace static reference const)
- `scr_`: `static` `constexpr` `reference`, can only refer to an object that is usable in constant expressions (`scr` - static constexpr reference)
- `gscr_`: `global` scope `static` `constexpr` `reference`, can only refer to an object that is usable in constant expressions (`gscp` - global static constexpr reference)
- `nscr_`: `namespace` scope `static` `constexpr` `reference`, can only refer to an object that is usable in constant expressions (`nscp` - namespace static constexpr reference)

### Function parameter prefixes

- `f_`: `function` parameter (`f` - function)
- `cf_`: `const` `function` parameter (`cf` - const function)
- `pf_`: `pointer` `function` parameter (`pf` - pointer function)
- `pcf_`: `pointer` to `const` object `function` parameter (`pcf` - pointer const function)
- `cpf_`: `const` `pointer` `function` parameter (`cpf` - const pointer function)
- `cpcf_`: `const` `pointer` to `const/constexpr` object `function` parameter (`cpcf` - const pointer const function)
- `rf_`: `reference` `function` parameter (`rf` - reference function)
- `rcf_`: `reference` to `const/constexpr` object `function` parameter (`rcf` - reference const function)
- `ef_`: `enum` `function` parameter (`ef` - enum function)
- `cef_`: `const` `enum` `function` parameter (`cef` - const enum function)

### Type prefixes

- `C_`: `class` (`C` - Class)
- `S_`: `struct` (`S` - Struct)
- `E_`: `enum` class (`E` - Enum)

### Type alias (`using`/`typedef`) prefixes

- `TA_`: some `type` `alias` (`TA` - Type Alias)

### Template parameter prefixes

- `T_`: `type` template parameter (`T` - Type)
- `TP_`: `type` template parameter `pack` (`TP` - Type Pack)
- `NT_`: `non-type` template parameter (`NT` - Non Type)
- `NTP_`: `non-type` template parameter `pack` (`NTP` - Non Type Pack)
- `TT_`: `template` template parameter (`TT` - TemplaTe)
- `TTP_`: `template` template parameter `pack` (`TTP` - TemplaTe Pack)

## Files

| Entity | Convention | Example |
|--------|------------|---------|
| Implementation/Source file name | noun in `snake_case.cpp` style-form | `frame_renderer.cpp` |
| Header file name | noun in `snake_case.hpp` style-form | `frame_renderer.hpp` |

## Types

| Entity | Convention | Example |
|--------|------------|---------|
| Class name | noun in `C_PascalCase` style-form | `C_FrameRenderer` |
| Struct name | noun in `S_PascalCase` style-form | `S_ProfileInfo` |
| Enum-class name | noun in `E_PascalCase` style-form | `E_FileType` |

## Macros

| Entity | Convention | Example |
|--------|------------|---------|
| Object-like macro name | noun in `macro_UPPER_SNAKE_CASE` style-form | `macro_MAX_BUFFER_SIZE` |
| Function-like macro name | imperative verb in `macro_camelCase()` style-form | `macro_saveData()` |

## Functions/Methods

| Entity | Convention | Example |
|--------|------------|---------|
| Function/Method name | imperative verb in `camelCase()` style-form | `sendRequest()` |
| Function/Method non-const && non-reference && non-pointer parameter name | noun in `camelCase` style-form | `firstArg` |
| Function/Method const && non-reference && non-pointer parameter name | noun in `c_camelCase` style-form | `c_secondArg` |
| Function/Method reference-to-data parameter name | noun in `r_camelCase` style-form | `r_thirdArg` |
| Function/Method reference-to-const-data parameter name | noun in `rс_camelCase` style-form | `rc_fifthArg` |
| Function/Method pointer-to-data parameter name | noun in `p_camelCase` style-form | `p_seventhArg` |
| Function/Method const-pointer-to-data parameter name | noun in `cp_camelCase` style-form | `cp_eighthArg` |
| Function/Method const-pointer-to-const-data parameter name | noun in `cpc_camelCase` style-form | `cpc_ninthArg` |
| Function/Method const-ptr-to-const parameter name | noun in `cPtrToC_camelCase` style-form | `cPtrToC_tenthArg` |

## Compile-time constants

| Entity | Convention | Example |
|--------|------------|---------|
| Enum-field name | any name in `enumerator_UPPER_SNAKE_CASE` style-form | `enumerator_DEEP_PURPLE` |
| Local compile-time const (constexpr/consteval/etc.) variable name | noun in `compile_camelCase` style-form | `compile_defaultTimeout` |
| Global compile-time const (constexpr/consteval/etc.) variable name | noun in `compile_PascalCase` style-form | `compile_DefaultTimeout` |
| Local compile-time const (constexpr/consteval/etc.) pointer name | noun in `compilePtr_camelCase` style-form | `compilePtr_defaultTimeout` |

## Run-time constants

| Entity | Convention | Example |
|--------|------------|---------|
| Local run-time const variable name | noun in `c_camelCase` style-form | `c_userName` |
| Global run-time const variable name | noun in `c_PascalCase` style-form | `c_UserName` |
| Local run-time const pointer name | noun in `cPtr_camelCase` style-form | `cPtr_userName` |
| Global run-time const pointer name | noun in `cPtr_PascalCase` style-form | `cPtr_UserName` |

## Local variables

## Global variables

## Template parameters

---

???

| Entity | Convention | Example |
|--------|------------|---------|
| Local non-const variable | noun in `camelCase` style-form | `userName` |
| Global non-const-variable | g_camelCase noun | `g_userName` |
| Global run-time const-variable | g_kPascalCase noun | `g_kUserName` |
| Non-const func-arg | camelCase noun | `firstArg` |
| Const arg/param | kPascalCase noun | `kSecondArg` |
| Class non-const data member | m_camelCase | `m_bufferSize` |
| Class run-time/compile-time const data member | m_kPascalCase | `m_kBufferSize` |
| Static non-const-variable | s_camelCase | `s_bufferSize` |
| Static run-time/compile-time const-variable | s_kPascalCase | `s_kBufferSize` |
| Namespaces | snake\_case | `fast_engine` |
