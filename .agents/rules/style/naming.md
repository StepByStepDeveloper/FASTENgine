# Naming Conventions

## Identifier prefixes

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
- `a`: variable in `anonymous` (unnamed) namespace (`a` - `a`nonymous)

Example 1: `g_someVar` - variable in the `global` namespace with name `someVar`

Example 2: `n_someVar` - variable in the `named` namespace with name `someVar`

Example 3: `a_someVar` - variable in the `anonymous` namespace with name `someVar`

**Important notice for the `a` prefix**:

Variables declared inside an anonymous (unnamed) namespace have internal linkage by definition — the compiler guarantees this automatically, so there is no need (and it is an error) to additionally apply the `static` (`s`) storage-class prefix. The `a` prefix is therefore mutually exclusive with `static` (`s`) and `extern` (`x`) storage class prefixes (see the storage-class prefixes below). An anonymous-namespace variable with internal-linkage storage is written `a_…`, never `as_…`.

**Important notice for local (function/block) scope**:

Variables declared inside a function or block scope are *block-scoped*: they have no linkage and are not members of any namespace. They intentionally **omit the scope prefix** entirely. The prefix order for a local variable starts at the `storage-class-prefix` slot (e.g., a `static` local is `s_someVar`, never `gs_someVar`); an ordinary local uses no leading scope/storage prefix at all (e.g., `someVar`). Recall that the minimal forms shown in the [Non-Member variable naming conventions](#non-member-variable-naming-conventions) table (such as `e_operatingMode`, `p_dataBuffer`) are valid only at local scope.

#### Storage class prefixes

- `s`: `static` variable (`s` - `s`tatic)
- `t`: `thread_local` variable (`t` - `t`hread_local)
- `st`: `static` `thread_local` variable (`st` - `s`tatic `t`hread_local)
- `x`: `extern` variable (`x` - e`x`tern)
- `xt`: `extern` `thread_local` variable (`xt` - e`x`tern `t`hread_local)

Example: `st_someVar` - `static` `thread_local` variable with name `someVar`

**Important notice for `s` prefix at namespace scope**:

All namespace-scope variables in C++ inherently have static storage duration. However, the `s` prefix at namespace scope (e.g., `gs_someVar` or `ns_someVar`) additionally indicates internal linkage — the variable is declared with the `static` keyword and is visible only within the current translation unit. This is a crucial distinction for large projects with multiple source files. The same reasoning applies to both the `global` (`g`) and the `named` (`n`) scope prefixes.

**Important notice for `x` prefix**:

The `x` prefix marks an `extern` *declaration* — a reference to a variable defined in another translation unit. The `extern` specifier requests external linkage, which is the opposite of what `static` requests at namespace scope; therefore the `s` and `x` prefixes are mutually exclusive and never combined. The `x` prefix is only valid on declarations, never on the corresponding definition (the definition is named according to its own scope/storage, typically with no storage-class prefix). The `xt` prefix marks a declaration of a `thread_local` variable defined in another translation unit.

Example: `gx_someVar` - `extern` variable in a `global` namespace with name `someVar` (declared in this translation unit, defined elsewhere)
Example: `nxt_someVar` - `extern` `thread_local` variable in a `named` namespace with name `someVar`

#### cv-qualifier prefixes

- `c`: `const` variable (`c` - `c`onst)
- `v`: `volatile` variable (`v` - `v`olatile)
- `cv`: `const` `volatile` variable (`cv` - `c`onst `v`olatile)

Example: `cv_someVar` - `const` `volatile` variable with name `someVar`

#### Enum prefixes

- `e`: variable of `enum` or `enum class` type (`e` - `e`num)

Example: `e_someVar` - variable of `enum` (or `enum class`) type with name `someVar`

##### Rationale for enum variable prefix

The `e` prefix on a variable (e.g., `e_varName`) makes it always possible to recognize that the variable is an enumeration. This is especially important when the variable is of a plain `enum` (not `enum class`), because plain enumerators can be assigned directly as `VAL` instead of `E_EnumType::VAL`. If a reader sees `var = VAL`, they might not realize variable is an enumeration because in such representation it may be some constant, not enumeration. Utilization of `e` prefix (`e_var = VAL`) solves that problem.

#### Pointer prefixes

- `p`: `pointer` to object of `class`/`struct`/`union`/`primitive` type (`p` - `p`ointer)
- `pc`: `pointer` to object of `const` `class`/`struct`/`union`/`primitive` type (`pc` - `p`ointer `c`onst)
- `pv`: `pointer` to object of `volatile` `class`/`struct`/`union`/`primitive` type (`pv` - `p`ointer `v`olatile)
- `pcv`: `pointer` to object of `const` `volatile` `class`/`struct`/`union`/`primitive` type (`pcv` - `p`ointer `c`onst `v`olatile)
- `pe`: `pointer` to object of `enum` (or `enum class`) type (`pe` - `p`ointer `e`num)
- `pce`: `pointer` to object of `const` `enum` (or `enum class`) type (`pce` - `p`ointer `c`onst `e`num)
- `pve`: `pointer` to object of `volatile` `enum` (or `enum class`) type (`pve` - `p`ointer `v`olatile `e`num)
- `pcve`: `pointer` to object of `const` `volatile` `enum` (or `enum class`) type (`pcve` - `p`ointer `c`onst `v`olatile `e`num)

Notice: pointer prefixes are applicable for smart pointers

Example: `pcve_someVar` - `pointer to object of const-volatile-enum type` with name `someVar`

#### Reference prefixes

- `r`: `reference` to object of `class`/`struct`/`union`/`primitive` type (`r` - `r`eference)
- `rc`: `reference` to object of `const` `class`/`struct`/`union`/`primitive` type (`rc` - `r`eference `c`onst)
- `rv`: `reference` to object of `volatile` `class`/`struct`/`union`/`primitive` type (`rv` - `r`eference `v`olatile)
- `rcv`: `reference` to object of `const` `volatile` `class`/`struct`/`union`/`primitive` type (`rcv` - `r`eference `c`onst `v`olatile)
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

Variable `gscvpcve_someVar` is `global`-scope, internal-linkage (`static`), `const volatile` pointer to an object of `const-volatile-enum` type, with name `someVar`:

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

Variable `gsrcve_someVar` is `global`-scope, internal-linkage (`static`) reference to an object of `const-volatile-enum` type, with name `someVar`:

- variable has `global` scope
- variable has internal linkage (`static`)
- variable has `reference` type
- variable refers to object of `const-volatile-enum` type, specifically `E_DeviceState`

### Types

Possible type cases:

- `type-name`: [`type-prefix`]_SomeType
- `type-alias-name`: [`type-alias-prefix`]_SomeType

#### Type prefixes

- `C`: `class` (`C` - `C`lass)
- `S`: `struct` (`S` - `S`truct)
- `E`: `enum` or `enum class` (`E` - `E`num)
- `U`: `union` (`U` - `U`nion)

Example 1:

```C++
enum class E_SomeType { Enum1, Enum2};

const E_SomeType gce_someVar = E_SomeType::Enum1;
```

- `E_SomeType`: An `enum class` type with name `SomeType`
- `gce_someVar`: A `global const enum` variable (instance) of `enum class` type (`E_SomeType`), marked with the `enum-prefix` (`e`)

Example 2:

```C++
class C_SomeType {};

C_SomeType g_var;

const C_SomeType* gpc_someVar = &g_var;
```

- `C_SomeType`: A `class` type with name `SomeType`
- `g_var`: A `global` variable (instance) of `class` type (`C_SomeType`)
- `gpc_someVar`: A `global pointer to const` object of `class` type (`C_SomeType`), marked with the `pointer-to-const` variant of the `pointer-prefix` (`pc`)

Example 3:

```C++
struct S_SomeType {};

S_SomeType g_var;

const S_SomeType& grc_someVar = g_var;
```

- `S_SomeType`: A `struct` type with name `SomeType`
- `g_var`: A `global` variable (instance) of `struct` type (`S_SomeType`)
- `grc_someVar`: A `global reference to const` object of `struct` type (`S_SomeType`), marked with the `reference-to-const` variant of the `reference-prefix` (`rc`)

#### Type alias prefixes (prefixes for types created via `using`/`typedef` keywords)

- `TA`: `type` `alias` to some primitive type (`TA` - `T`ype `A`lias)
- `TAC`: `type` `alias` to some `class` type (`TAC` - `T`ype `A`lias `C`lass)
- `TAS`: `type` `alias` to some `struct` type (`TAS` - `T`ype `A`lias `S`truct)
- `TAE`: `type` `alias` to some `enum` type (`TAE` - `T`ype `A`lias `E`num)
- `TAU`: `type` `alias` to some `union` type (`TAU` - `T`ype `A`lias `U`nion)
- `TAP`: `type` `alias` to some `pointer` type (`TAP` - `T`ype `A`lias `P`ointer)
- `TAR`: `type` `alias` to some `reference` type (`TAR` - `T`ype `A`lias `R`eference)
- `TAF`: `type` `alias` to some `function` type (`TAF` - `T`ype `A`lias `F`unction)

**Notice for aliases of aliases**: A `using`/`typedef` declaration introduces no new type — an alias is just another name for the underlying type. Therefore, an alias of another alias must be named according to the *resolved* underlying type's category (e.g., aliasing a `TAC_SomeType` still yields a `TAC_…` name, not a separate `TAA` prefix). There is intentionally no `TAA` prefix.

Example 1:

```C++
enum class E_SomeType { Enum1, Enum2};

using TAE_SomeType = E_SomeType;

E_SomeType ge_var = E_SomeType::Enum1;

const TAE_SomeType gce_someVar = ge_var;
```

- `TAE_SomeType`: A `type alias` for `enum class` type (`E_SomeType`)
- `ge_var`: A `global enum` variable (instance) of `enum class` type (`E_SomeType`), marked with the `enum-prefix` (`e`)
- `gce_someVar`: A `global const enum` variable (instance) of `enum class` type (`E_SomeType`), marked with the `enum-prefix` (`e`)

Example 2:

```C++
class C_SomeType {};

using TAC_SomeType = C_SomeType;

C_SomeType g_var;

const TAC_SomeType* gpc_someVar = &g_var;
```

- `TAC_SomeType`: A `type alias` for `class` type (`C_SomeType`)
- `g_var`: A `global` variable (instance) of `class` type (`C_SomeType`)
- `gpc_someVar`: A `global pointer to const` object of `class` type (`C_SomeType`), marked with the `pointer-to-const` variant of the `pointer-prefix` (`pc`)

Example 3:

```C++
struct S_SomeType {};

using TAS_SomeType = S_SomeType;

S_SomeType g_var;

const TAS_SomeType& grc_someVar = g_var;
```

- `TAS_SomeType`: A `type alias` for `struct` type (`S_SomeType`)
- `g_var`: A `global` variable (instance) of `struct` type (`S_SomeType`)
- `grc_someVar`: A `global reference to const` object of `struct` type (`S_SomeType`), marked with the `reference-to-const` variant of the `reference-prefix` (`rc`)

### Template parameters

#### Type template parameter prefixes

- `TTP`: `type` `template` `parameter` (`TTP` - `T`ype `T`emplate `P`arameter)
- `TTPP`: `type` `template` `parameter` `pack` (`TTPP` - `T`ype `T`emplate `P`arameter `P`ack)

#### Non-Type template parameter prefixes

- `NTTP`: `non` `type` `template` `parameter` (`NTTP` - `N`on `T`ype `T`emplate `P`arameter)
- `NTTPP`: `non` `type` `template` `parameter` `pack` (`NTTPP` - `N`on `T`ype `T`emplate `P`arameter `P`ack)

#### Template template parameter prefixes

- `TeTP`: `template` `template` `parameter` (`TeTP` - `Te`mplate `T`emplate `P`arameter)
- `TeTPP`: `template` `template` `parameter` `pack` (`TeTPP` - `Te`mplate `T`emplate `P`arameter `P`ack)

## File naming conventions

| Entity                          | Convention                          | Example              |
|:------------------------------- | ----------------------------------- | -------------------- |
| Implementation/Source file name | noun in `snake_case.cpp` style-form | `frame_renderer.cpp` |
| Header file name                | noun in `snake_case.hpp` style-form | `frame_renderer.hpp` |

## Namespace naming conventions

| Entity     | Convention   | Example          |
|:---------- | ------------ | ---------------- |
| Namespaces | `snake_case` | `frame_renderer` |

## Type naming conventions

| Entity          | Convention                           | Example             |
|:--------------- | ------------------------------------ | ------------------- |
| Type name       | noun in `type-name` style-form       | `C_FrameRenderer`   |
| Type alias name | noun in `type-alias-name` style-form | `TAC_FrameRenderer` |

## Function-like Macro and Function/Method naming conventions

| Entity                   | Convention                                         | Example         |
|:------------------------ | -------------------------------------------------- | --------------- |
| Function-like macro name | imperative verb in `UPPER_SNAKE_CASE()` style-form | `SAVE_DATA()`   |
| Function/Method name     | imperative verb in `camelCase()` style-form        | `sendRequest()` |

## Object-like Macro and Enumerator naming conventions

| Entity                              | Convention                                | Example           |
|:----------------------------------- | ----------------------------------------- | ----------------- |
| Object-like macro name              | noun in `UPPER_SNAKE_CASE` style-form     | `MAX_BUFFER_SIZE` |
| Enumerator name for enum-class type | any name in `PascalCase` style-form       | `DeepPurple`      |
| Enumerator name for enum type       | any name in `UPPER_SNAKE_CASE` style-form | `DEEP_PURPLE`     |

### Rationale for enumerator naming

For backward compatibility with C-style conventions, plain `enum` enumerators use `UPPER_SNAKE_CASE` (e.g., `DEEP_PURPLE`). For `enum class` enumerators, the mandatory type-name qualifier `E_EnumType::` allows the enumerator name itself to be written in `PascalCase` instead of `UPPER_SNAKE_CASE`, yielding the full form `E_Color::DeepPurple`.

## Non-Member variable naming conventions

| Entity                  | Convention                         | Example           |
|:----------------------- | ---------------------------------- | ----------------- |
| Enum variable name      | noun in `enum-var` style-form      | `e_operatingMode` |
| Pointer variable name   | noun in `pointer-var` style-form   | `p_dataBuffer`    |
| Reference variable name | noun in `reference-var` style-form | `r_dataBuffer`    |
| Ordinary variable name  | noun in `normal-var` style-form    | `operatingMode`   |

## Member variable naming conventions

The base name of a member variable follows the same prefix rules as non-member variables (prefixes + meaningful name in `camelCase`). On top of that, the requirements below apply.

**Important notice for member scope and storage prefixes**:

Class members are *class-scoped*, not namespace-scoped, so they intentionally **omit the `scope-prefix`** (`g` / `n` / `a`) — none of those applies to a field. What remains is the `storage-class-prefix` slot:

- An ordinary (instance) non-static member uses **no storage-class prefix** (e.g., `operatingMode`, `pe_dataBuffer`).
- A `static` class member uses the **`s`** storage-class prefix (e.g., `s_instanceCount`). Note carefully: at *namespace* scope `s` means internal linkage, but a `static` class member has **external linkage**. The `s` prefix on a member therefore denotes *class-level (shared) storage only*, not internal linkage — there is no contradiction because the scope prefix is absent and the class scope, not the storage prefix, governs linkage. The `x` (`extern`) prefix is **never** used on members: `static` members are defined exactly once and resolved by the linker; an `extern` declaration of one is written in the header with the plain `s` prefix and defined in one source file with the same `s` prefix (the keyword `static` is omitted at the definition).
- `thread_local` members additionally carry **`t`** (e.g., `t_threadStorage`), and `static thread_local` members carry **`st`** (e.g., `st_threadCache`), mirroring the namespace-scope storage-class prefixes.

These storage prefixes occupy the same slot as for non-members — between the (absent) `scope-prefix` and the `cv-qualifier-prefix`, i.e. `[scope: omitted][storage-class-prefix][cv-qualifier-prefix][enum/pointer/reference-prefix]_camelCase`. The access suffix (`_` / `__`) is always appended last, after the full prefixed base name (see [Members combining prefixes and access suffixes](#members-combining-prefixes-and-access-suffixes)).

- Non-`static` fields declared in a class **must** be accessed inside class methods exclusively via the `this->` qualifier (e.g., `this->operatingMode`). The `this->` qualifier **must never** be omitted so that it is always obvious an access refers to a class field.
- `static` members are **not** accessed via `this->` (they have no instance). They **must** be qualified with their enclosing class name (e.g., `C_SomeType::s_instanceCount`) even from within the class's own methods, so that the access is unambiguously a class-level entity.
- `public` fields **must not** add any suffix.
- `protected` fields **must** have the suffix `_` (e.g., `operatingMode_`).
- `private` fields **must** have the suffix `__` (e.g., `operatingMode__`).

| Access level | Inside class methods             | Outside the class (via object/pointer)                                                              |
|:------------ | -------------------------------- | --------------------------------------------------------------------------------------------------- |
| `public`     | `this->[member-variable-name]`   | `obj.[member-variable-name]` / `ptr->[member-variable-name]`                                        |
| `protected`  | `this->[member-variable-name]_`  | `obj.[member-variable-name]_` / `ptr->[member-variable-name]_` (accessible only from derived class) |
| `private`    | `this->[member-variable-name]__` | Not accessible                                                                                      |

### `mutable` members

The `mutable` keyword is orthogonal to access level and to all prefix categories: it governs whether a field may be modified through a `const`-qualified method, not the field's scope, storage, or type. `mutable` members therefore follow exactly the same naming rules as non-`mutable` members of the same access level; the `mutable` qualifier is intentionally not encoded in the name.

Example:

```C++
class C_Cache {
public:
    mutable std::size_t accessCount;       // mutable public:    no suffix
protected:
    mutable E_CacheState e_state_;         // mutable protected: suffix `_`
private:
    mutable E_CacheState e_replacement__;  // mutable private:   suffix `__`
};

// inside a const method:
// this->accessCount++;
// this->e_state_;
// this->e_replacement__;
```

### Members combining prefixes and access suffixes

When a member carries both a leading prefix (e.g., a `pointer-prefix` or `enum-prefix`) and an access suffix (`_` / `__`), the access suffix is appended *after* the full prefixed base name, in exactly the same position as for plain members.

Example:

```C++
class C_SomeType {
protected:
    E_OperatingMode* pe_operatingMode_;  // protected pointer member
private:
    E_OperatingMode e_targetState__;     // private enum-typed member
};

// access:
// this->pe_operatingMode_;
// this->e_targetState__;
```

## Template parameter naming conventions

| Entity                           | Convention                            | Example          |
|:-------------------------------- | ------------------------------------- | ---------------- |
| Type template parameter          | noun in `TTP_PascalCase` style-form   | `TTP_Value`      |
| Type template parameter pack     | noun in `TTPP_PascalCase` style-form  | `TTPP_Args`      |
| Non-type template parameter      | noun in `NTTP_PascalCase` style-form  | `NTTP_Count`     |
| Non-type template parameter pack | noun in `NTTPP_PascalCase` style-form | `NTTPP_Values`   |
| Template template parameter      | noun in `TeTP_PascalCase` style-form  | `TeTP_Allocator` |
| Template template parameter pack | noun in `TeTPP_PascalCase` style-form | `TeTPP_Policies` |
