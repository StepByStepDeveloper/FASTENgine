# Naming Conventions

## Naming prefixes

### Variables

Variable names may consist of a combination of prefixes in the following order of these prefix types (each type appears exactly once in the specified order):

- `normal-var` (non-enum and non-pointer and non-reference) variable: [`scope-prefix`][`storage-class-prefix`][`cv-qualifier-prefix`]_camelCase
- `enum-var` variable: [`scope-prefix`][`storage-class-prefix`][`cv-qualifier-prefix`][`enum-prefix`]_camelCase
- `pointer-var` variable: [`scope-prefix`][`storage-class-prefix`][`cv-qualifier-prefix`][`pointer-prefix`]_camelCase
- `reference-var` variable: [`scope-prefix`][`storage-class-prefix`][`reference-prefix`]_camelCase

**Important notice for references**:

Unlike pointers, references in C++ cannot carry cv-qualifiers (const, volatile) themselves. Therefore, the [`cv-qualifier-prefix`] is intentionally omitted from the reference variable naming formula. The cv-qualifiers of the referenced object are fully captured by the [`reference-prefix`] (e.g., `rc` for `reference to const`, `rcv` for `reference to const volatile`). Never apply [`cv-qualifier-prefix`] before [`reference-prefix`].

#### Scope prefixes

- `g`: variable in `global` namespace (`g` - `g`lobal)
- `n`: variable in `named` namespace (`n` - `n`amed)

Example: `g_someVar` - variable in the `global` namespace with name `someVar`

#### Storage class prefixes

- `s`: `static` variable (`s` - `s`tatic)
- `t`: `thread_local` variable (`t` - `t`hread_local)
- `st`: `static` `thread_local` variable (`st` - `s`tatic `t`hread_local)

Example: `st_someVar` - `static` `thread_local` variable with name `someVar`

**Important notice for `s` prefix in global scope**:

All global variables in C++ inherently have static storage duration. However, the `s` prefix in global scope (e.g., `gs_someVar`) additionally indicates internal linkage — the variable is declared with the `static` keyword and is visible only within the current translation unit. This is a crucial distinction for large projects with multiple source files.

#### cv-qualifier prefixes

- `c`: `const` variable (`c` - `c`onst)
- `v`: `volatile` variable (`v` - `v`olatile)
- `cv`: `const` `volatile` variable (`cv` - `c`onst `v`olatile)

Example: `cv_someVar` - `const` `volatile` variable with name `someVar`

#### Enum prefixes

- `e`: variable of `enum` or `enum class` type (`e` - `e`num)

Example: `e_someVar` - variable of `enum` type with name `someVar`

#### Pointer prefixes

- `p`: `pointer` to object of `class`/`struct`/`primitive` type (`p` - `p`ointer)
- `pc`: `pointer` to object of `const` `class`/`struct`/`primitive` type (`pc` - `p`ointer `c`onst)
- `pv`: `pointer` to object of `volatile` `class`/`struct`/`primitive` type (`pv` - `p`ointer `v`olatile)
- `pcv`: `pointer` to object of `const` `volatile` `class`/`struct`/`primitive` type (`pcv` - `p`ointer `c`onst `v`olatile)
- `pe`: `pointer` to object of `enum` (or `enum class`) type (`pe` - `p`ointer `e`num)
- `pce`: `pointer` to object of `const` `enum` (or `enum class`) type (`pce` - `p`ointer `c`onst `e`num)
- `pve`: `pointer` to object of `volatile` `enum` (or `enum class`) type (`pve` - `p`ointer `v`olatile `e`num)
- `pcve`: `pointer` to object of `const` `volatile` `enum` (or `enum class`) type (`pcve` - `p`ointer `c`onst `v`olatile `e`num)

Notice: applicable for smart pointers

Example: `pcve_someVar` - `pointer to object of const-volatile-enum type` with name `someVar`

#### Reference prefixes

- `r`: `reference` to object of `class`/`struct`/`primitive` type (`r` - `r`eference)
- `rc`: `reference` to object of `const` `class`/`struct`/`primitive` type (`rc` - `r`eference `c`onst)
- `rv`: `reference` to object of `volatile` `class`/`struct`/`primitive` type (`rv` - `r`eference `v`olatile)
- `rcv`: `reference` to object of `const` `volatile` `class`/`struct`/`primitive` type (`rcv` - `r`eference `c`onst `v`olatile)
- `re`: `reference` to object of `enum` (or `enum class`) type (`re` - `r`eference `e`num)
- `rce`: `reference` to object of `const` `enum` (or `enum class`) type (`rce` - `r`eference `c`onst `e`num)
- `rve`: `reference` to object of `volatile` `enum` (or `enum class`) type (`rve` - `r`eference `v`olatile `e`num)
- `rcve`: `reference` to object of `const` `volatile` `enum` (or `enum class`) type (`rcve` - `r`eference `c`onst `v`olatile `e`num)

Example: `rcve_someVar` - `reference to object of const-volatile-enum type` with name `someVar`

#### Ultimate variable naming examples

Example 1:

```C++
enum E_DeviceState { STATE_IDLE, STATE_RUNNING, STATE_ERROR };

const volatile E_DeviceState gcve_targetState = STATE_IDLE;

static const volatile E_DeviceState* const volatile gscvpcve_someVar = &gcve_targetState;
```

Variable `gscvpcve_someVar` is `global static const volatile pointer to object of const-volatile-enum type` with name `someVar`:

- variable has `global` scope
- variable has internal linkage (`static`)
- variable has `const volatile` qualifiers
- variable has `pointer` type
- variable points to object of `const-volatile-enum` type, specifically `E_DeviceState`

Example 2:

```C++
enum E_DeviceState { STATE_IDLE, STATE_RUNNING, STATE_ERROR };

const volatile E_DeviceState gcve_targetState = STATE_IDLE;

static const volatile E_DeviceState& gsrcve_someVar = gcve_targetState;
```

Variable `gsrcve_someVar` is `global static reference to object of const-volatile-enum type` with name `someVar`:

- variable has `global` scope
- variable has internal linkage (`static`)
- variable has `reference` type
- variable refers to object of `const-volatile-enum` type, specifically `E_DeviceState`

### Types

Prefixes for types:

- `type-name`: [`type-prefix`]_SomeType
- `type-alias-name`: [`type-alias-prefix`]_SomeType

#### Type prefixes

- `C`: `class` (`C` - `C`lass)
- `S`: `struct` (`S` - `S`truct)
- `E`: `enum` or `enum class` (`E` - `E`num)

Example 1:

```C++
enum class E_SomeType { Enum1, Enum2};

const E_SomeType gce_someVar = E_SomeType::Enum1;
```

- `E_SomeType`: An `enum class` type with name `SomeType`
- `gce_someVar`: A `global scope const enum` variable (instance) of that `enum class` type, marked with the `enum-prefix`

Example 2:

```C++
class C_SomeType {};

C_SomeType g_var;

const C_SomeType* gpc_someVar = &g_var;
```

- `C_SomeType`: A `class` type with name `SomeType`
- `g_var`: A `global scope` variable (instance) of that `class` type
- `gpc_someVar`: A `global scope pointer to const` object of that `class` type, marked with the `pointer-prefix`

Example 3:

```C++
struct S_SomeType {};

S_SomeType g_var;

const S_SomeType& grc_someVar = g_var;
```

- `S_SomeType`: A `struct` type with name `SomeType`
- `g_var`: A `global scope` variable (instance) of that `struct` type
- `grc_someVar`: A `global scope reference to const` object of that `struct` type, marked with the `reference-prefix`

#### Type alias prefixes (prefixes for types created via `using`/`typedef` keywords)

- `TA`: `type` `alias` to some primitive type (`TA` - `T`ype `A`lias)
- `TAC`: `type` `alias` to some `class` type (`TAC` - `T`ype `A`lias `C`lass)
- `TAS`: `type` `alias` to some `struct` type (`TAS` - `T`ype `A`lias `S`truct)
- `TAE`: `type` `alias` to some `enum` type (`TAE` - `T`ype `A`lias `E`num)

Example 1:

```C++
enum class E_SomeType { Enum1, Enum2};

using TAE_SomeType = E_SomeType;

E_SomeType ge_var = E_SomeType::Enum1;

const TAE_SomeType gce_someVar = ge_var;
```

- `TAE_SomeType`: A `type alias` (`TA`) for an `enum class` type (`E`)
- `ge_var`: A `global scope enum` variable (instance) of that `enum class` type, marked with the `enum-prefix`
- `gce_someVar`: A `global scope const enum` variable (instance) of that `enum class` type, marked with the `enum-prefix`

Example 2:

```C++
class C_SomeType {};

using TAC_SomeType = C_SomeType;

C_SomeType g_var;

const TAC_SomeType* gpc_someVar = &g_var;
```

- `TAC_SomeType`: A `type alias` (`TA`) for a `class` type (`C`)
- `g_var`: A `global scope` variable (instance) of that `class` type
- `gpc_someVar`: A `global scope pointer to const` object of that `class` type, marked with the `pointer-prefix`

Example 3:

```C++
struct S_SomeType {};

using TAS_SomeType = S_SomeType;

S_SomeType g_var;

const TAS_SomeType& grc_someVar = g_var;
```

- `TAS_SomeType`: A `type alias` (`TA`) for a `struct` type (`S`)
- `g_var`: A `global scope` variable (instance) of that `struct` type
- `grc_someVar`: A `global scope reference to const` object of that `struct` type, marked with the `reference-prefix`

### Template parameters

#### Type template parameter prefixes

- `T`: `type` template parameter (`T` - `T`ype)
- `TP`: `type` template parameter `pack` (`TP` - `T`ype `P`ack)

#### Non-Type template parameter prefixes

- `NT`: `non-type` template parameter (`NT` - `N`on `T`ype)
- `NTP`: `non-type` template parameter `pack` (`NTP` - `N`on `T`ype `P`ack)

#### Template template parameter prefixes

- `TT`: `template` template parameter (`TT` - `T`empla`T`e)
- `TTP`: `template` template parameter `pack` (`TTP` - `T`empla`T`e `P`ack)

## File naming conventions

| Entity                          | Convention                          | Example              |
|:------------------------------- | ----------------------------------- | -------------------- |
| Implementation/Source file name | noun in `snake_case.cpp` style-form | `frame_renderer.cpp` |
| Header file name                | noun in `snake_case.hpp` style-form | `frame_renderer.hpp` |

## Namespace naming conventions

| Entity     | Convention   | Example       |
|:---------- | ------------ | ------------- |
| Namespaces | `snake_case` | `fast_engine` |

## Type naming conventions

| Entity          | Convention                                          | Example           |
|:--------------- | --------------------------------------------------- | ----------------- |
| Type name       | noun in `[type-prefix]_PascalCase` style-form       | `C_FrameRenderer` |
| Type alias name | noun in `[type-alias-prefix]_PascalCase` style-form | `TA_ProfileInfo`  |

## Functions/Method naming conventions

| Entity                   | Convention                                         | Example         |
|:------------------------ | -------------------------------------------------- | --------------- |
| Function-like macro name | imperative verb in `UPPER_SNAKE_CASE()` style-form | `SAVE_DATA()`   |
| Function/Method name     | imperative verb in `camelCase()` style-form        | `sendRequest()` |

## Constant naming conventions

| Entity                              | Convention                                | Example               |
|:----------------------------------- | ----------------------------------------- | --------------------- |
| Object-like macro name              | noun in `UPPER_SNAKE_CASE` style-form     | `MAX_BUFFER_SIZE`     |
| Enumerator name for enum-class type | any name in `PascalCase` style-form       | `E_Color::DeepPurple` |
| Enumerator name for enum type       | any name in `UPPER_SNAKE_CASE` style-form | `DEEP_PURPLE`         |

### Rationale for enumerator naming

The `e_` prefix on a variable (e.g., `e_varName`) makes it always possible to recognize that the variable is an enumeration. This is especially important when the variable is of a plain `enum` (not `enum class`), because plain enumerators can be assigned directly as `VAL` instead of `E_EnumType::VAL`. If a reader sees `var = VAL`, they might not realize it is an enumeration; `e_var = VAL` solves that problem.

For backward compatibility with C-style conventions, plain `enum` enumerators use `UPPER_SNAKE_CASE` (e.g., `DEEP_PURPLE`). For `enum class` variables, the mandatory scope prefix `E_EnumType::` allows the enumerator name itself to be written in `PascalCase` instead of `UPPER_SNAKE_CASE`, yielding the full form `E_Color::DeepPurple`.

## Non-Member variable naming conventions

| Entity                  | Convention                                                | Example           |
|:----------------------- | --------------------------------------------------------- | ----------------- |
| Enum variable name      | noun in `[scope][storage][cv][enum]_camelCase` style-form | `e_operatingMode` |
| Pointer variable name   | noun in `[scope][storage][cv][ptr]_camelCase` style-form  | `p_operatingMode` |
| Reference variable name | noun in `[scope][storage][ref]_camelCase` style-form      | `r_operatingMode` |
| Ordinary variable name  | noun in `[scope][storage][cv]_camelCase` style-form       | `operatingMode`   |

### Rationale for enum variable prefix

See the rationale under **Constant naming conventions / Rationale for enumerator naming**. The `e_` prefix on a non-member variable serves the same purpose: it makes the enumeration nature explicit at every use site.

## Member variable naming conventions

The base name of a member variable follows the same prefix rules as non-member variables (prefixes + meaningful name in `camelCase`). On top of that, the following requirements apply:

- Fields declared in a class **must** be accessed inside class methods exclusively via `this->variableName`. The `this->` qualifier **must never** be omitted so that it is always obvious an access refers to a class field.
- `public` fields **must not** add any suffix.
- `protected` fields **must** have the suffix `_` (e.g., `this->operatingMode_`).
- `private` fields **must** have the suffix `__` (e.g., `this->operatingMode__`).

| Access level | Inside class methods           | Outside the class (via object/pointer)                                               |
|:------------ | ------------------------------ | ------------------------------------------------------------------------------------- |
| `public`     | `this->[non-member-name]`      | `obj.[non-member-name]` / `obj->[non-member-name]`                                    |
| `protected`  | `this->[non-member-name]_`     | `obj.[non-member-name]_` / `obj->[non-member-name]_` (accessible only from derived) |
| `private`    | `this->[non-member-name]__`    | Not accessible                                                                        |

## Template parameter naming conventions

| Entity                           | Convention                            | Example          |
|:-------------------------------- | ------------------------------------- | ---------------- |
| Type template parameter          | noun in `T_PascalCase` style-form     | `T_Value`        |
| Type template parameter pack     | noun in `TP_PascalCase` style-form    | `TP_Args`        |
| Non-type template parameter      | noun in `NT_PascalCase` style-form    | `NT_Count`       |
| Non-type template parameter pack | noun in `NTP_PascalCase` style-form   | `NTP_Values`     |
| Template template parameter      | noun in `TT_PascalCase` style-form    | `TT_Allocator`   |
| Template template parameter pack | noun in `TTP_PascalCase` style-form   | `TTP_Policies`   |

### Rationale for template parameter naming

Template parameters are prefixed so that their role is immediately recognizable inside template declarations. `T_` marks a single type parameter, `TP_` a type parameter pack, `NT_` a single non-type parameter, `NTP_` a non-type parameter pack, `TT_` a template template parameter, and `TTP_` a template template parameter pack. Using `PascalCase` for the descriptive part keeps template parameters visually distinct from both runtime variables (`camelCase`) and concrete type names (`Prefix_PascalCase`).

## Examples
