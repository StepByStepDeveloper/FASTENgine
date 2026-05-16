# Naming Conventions

## Naming prefixes and their combinations

### Variable prefixes

- `c_`: const/constexpr variable
- `s_`: static variable
- `sc_`: static const/constexpr variable

### Macro prefixes

- `macro_`: Object-like or function-like macro

### Enum prefixes

- `e_`: enum variable
- `ce_`: const/constexpr enum variable
- `se_`: static enum variable
- `sce_`: static const/constexpr enum variable

### Pointer prefixes

- `p_`: pointer
- `pc_`: pointer to const/constexpr object
- `cp_`: const/constexpr pointer
- `cpc_`: const/constexpr pointer to const/constexpr object
- `sp_`: static pointer
- `spc_`: static pointer to const/constexpr object
- `scp_`: static const/constexpr pointer
- `scpc_`: static const/constexpr pointer to const/constexpr object

### Reference prefixes

- `r_`: reference
- `rc_`: reference to const/constexpr object
- `cr_`: constexpr reference (can only refer to an object that is usable in constant expressions)
- `sr_`: static reference
- `src_`: static reference to const/constexpr object
- `scr_`: static constexpr reference (can only refer to an object that is usable in constant expressions)

### Type prefixes

- `C_`: class
- `S_`: struct
- `E_`: enum class

### Type alias (`using`/`typedef`) prefixes

- `TA_`: some type alias

### Template parameter prefixes

- `T_`: type parameter
- `TP_`: type parameter pack
- `NT_`: non-type parameter
- `NTP_`: non-type parameter pack
- `TT_`: template template parameter
- `TTP_`: template template parameter pack

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
