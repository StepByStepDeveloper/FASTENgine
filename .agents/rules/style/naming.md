# Naming Conventions

## Files

| Entity | Convention | Example |
|--------|------------|---------|
| Implementation/Source file name | noun in `snake_case.cpp` style-form | `frame_renderer.cpp` |
| Header file name | noun in `snake_case.hpp` style-form | `frame_renderer.hpp` |

## Types

| Entity | Convention | Example |
|--------|------------|---------|
| Class name | noun in `Class_PascalCase` style-form | `Class_FrameRenderer` |
| Struct name | noun in `Struct_PascalCase` style-form | `Struct_ProfileInfo` |
| Enum-class name | noun in `Enum_PascalCase` style-form | `Enum_FileType` |

## Macros

| Entity | Convention | Example |
|--------|------------|---------|
| Basic macro name | noun in `macro_UPPER_SNAKE_CASE` style-form | `macro_MAX_BUFFER_SIZE` |
| Function-like macro name | imperative verb in `macro_camelCase()` style-form | `macro_saveData()` |

## Functions/Methods

| Entity | Convention | Example |
|--------|------------|---------|
| Function/Method name | imperative verb in `camelCase()` style-form | `sendRequest()` |
| Function/Method non-const && non-ref && non-ptr parameter name | noun in `camelCase` style-form | `firstArg` |
| Function/Method const && non-ref && non-ptr parameter name | noun in `const_camelCase` style-form | `const_secondArg` |
| Function/Method non-const-ref-to-non-const parameter name | noun in `ref_camelCase` style-form | `ref_thirdArg` |
| Function/Method const-ref-to-non-const parameter name | noun in `cRef_camelCase` style-form | `cRef_fourthArg` |
| Function/Method non-const-ref-to-const parameter name | noun in `refToC_camelCase` style-form | `refToC_fifthArg` |
| Function/Method const-ref-to-const parameter name | noun in `cRefToC_camelCase` style-form | `cRefToC_sixthArg` |
| Function/Method non-const-ptr-to-non-const parameter name | noun in `ptr_camelCase` style-form | `ptr_seventhArg` |
| Function/Method const-ptr-to-non-const parameter name | noun in `cPtr_camelCase` style-form | `cPtr_eighthArg` |
| Function/Method non-const-ptr-to-const parameter name | noun in `ptrToC_camelCase` style-form | `ptrToC_ninthArg` |
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
| Local run-time const variable name | noun in `const_camelCase` style-form | `const_userName` |
| Global run-time const variable name | noun in `const_PascalCase` style-form | `const_UserName` |
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
