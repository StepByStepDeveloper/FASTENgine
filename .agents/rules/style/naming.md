# Naming Conventions

## Identifier prefixes

### Variables

Variable names may consist of a combination of prefixes in the following order of these prefix types (each applicable type appears at most once, in the specified order, with the cv-qualifier-prefix slot intentionally absent for references — see the notice below):

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

#### CV-qualifier prefixes

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

**Important notice for member-method calls**:

Non-`static` member methods **must** be called from within the class's own methods exclusively via the `this->` qualifier (e.g., `this->resizeBuffer()`). The `this->` qualifier **must never** be omitted so that it is always obvious a call targets an instance method rather than a free function. `static` member methods, conversely, **must** be qualified with the enclosing class name (e.g., `C_SomeType::create()`) and **must never** be called via `this->`.

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
- `thread_local` members additionally carry **`t`** (e.g., `t_threadStorage`), and `static thread_local` members carry **`st`** (e.g., `st_cache`), mirroring the namespace-scope storage-class prefixes.

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

## Ultimate Compilable Example

A single, self-contained translation unit (example) that exercises every naming convention defined in this document. This example is artificial by design. The file-name convention is represented by the hypothetical artifact name `ultimate_example.cpp`, and the namespace-name convention is demonstrated by the `snake_case` namespaces below.

```C++
// ============================================================================
// Ultimate Compilable Example
// File-name convention: ultimate_example.cpp  Namespace convention: snake_case
// ============================================================================

// ---- Macros (object-like + function-like) ----
#define MAX_BUFFER_SIZE 256                                           // object-like macro: UPPER_SNAKE_CASE
#define SAVE_DATA(dst, src) ((void)((dst) = (src)))                   // function-like macro: UPPER_SNAKE_CASE()

// ---- Types ----
enum       E_DeviceState { STATE_IDLE, STATE_RUNNING, STATE_ERROR };  // plain enum; enumerators UPPER_SNAKE_CASE
enum class E_Color       { DeepPurple, LightBlue };                   // enum class; enumerators PascalCase
struct     S_Point       { int x; int y; };                           // struct type
union      U_Packet      { int raw; float floating; };                // union type
class      C_Renderer;                                                // class type (forward)

// ---- Type aliases (using) ----
using TA_Count     = unsigned;       // alias to primitive
using TAC_Renderer = C_Renderer;     // alias to class
using TAS_Point    = S_Point;        // alias to struct
using TAE_Color    = E_Color;        // alias to enum
using TAU_Packet   = U_Packet;       // alias to union
using TAP_IntPtr   = int*;           // alias to pointer
using TAR_IntRef   = int&;           // alias to reference
using TAF_BinaryOp = int(int, int);  // alias to function

// ============================================================================
// Global-namespace variables
// ============================================================================
int                     g_someVar   = 20;                    // scope = g
static int              gs_someVar  = 21;                    // g + static(internal linkage)
thread_local int        gt_someVar  = 22;                    // g + thread_local
static thread_local int gst_someVar = 23;                    // g + static thread_local
const int               gc_someVar  = 24;                    // g + const
volatile int            gv_someVar  = 25;                    // g + volatile
const volatile int      gcv_someVar = 0;                     // g + const volatile

extern int              gx_someVar;                          // extern declaration (defined elsewhere)
extern thread_local int gxt_someVar;                         // extern thread_local declaration

// global enum variables
E_DeviceState                ge_someState     = STATE_IDLE;  // scope = g + enum
const E_DeviceState          gce_someState    = STATE_IDLE;  // g + const + enum
const volatile E_DeviceState gcve_targetState = STATE_IDLE;  // g + const volatile + enum

// targets for pointers / references
int                          g_intTarget     = 30;
const int                    gc_intTarget    = 31;
volatile int                 gv_intTarget    = 32;
const volatile int           gcv_intTarget   = 0;

// states for pointers / references
E_DeviceState                ge_state   = STATE_RUNNING;
const E_DeviceState          gce_state  = STATE_RUNNING;
volatile E_DeviceState       gve_state  = STATE_RUNNING;
const volatile E_DeviceState gcve_state = STATE_RUNNING;

// pointer variables
int*                                                gp_intTarget   = &g_intTarget;    // global pointer
const int*                                          gpc_intTarget  = &gc_intTarget;   // global pointer to const
volatile int*                                       gpv_intTarget  = &gv_intTarget;   // global pointer to volatile
const volatile int*                                 gpcv_intTarget = &gcv_intTarget;  // global pointer to const volatile
E_DeviceState*                                      gpe_state      = &ge_state;       // global pointer to enum
const E_DeviceState*                                gpce_state     = &gce_state;      // global pointer to const enum
volatile E_DeviceState*                             gpve_state     = &gve_state;      // global pointer to volatile enum
const volatile E_DeviceState*                       gpcve_state    = &gcve_state;     // global pointer to const volatile enum
static const volatile E_DeviceState* const volatile gscvpcve_state = &gcve_state;     // global static const volatile pointer to const volatile enum

// reference variables — no cv-qualifier prefix slot for references
int&                                 gr_intTarget   = g_intTarget;    // global reference
const int&                           grc_intTarget  = gc_intTarget;   // global reference to const
volatile int&                        grv_intTarget  = gv_intTarget;   // global reference to volatile
const volatile int&                  grcv_intTarget = gcv_intTarget;  // global reference to const volatile
E_DeviceState&                       gre_state      = ge_state;       // global reference to enum
const E_DeviceState&                 grce_state     = gce_state;      // global reference to const enum
volatile E_DeviceState&              grve_state     = gve_state;      // global reference to volatile enum
const volatile E_DeviceState&        grcve_state    = gcve_state;     // global reference to const volatile enum
static const volatile E_DeviceState& gsrcve_state   = gcve_state;     // global static reference to const volatile enum

// ============================================================================
// Named namespace (snake_case): frame_renderer
// ============================================================================
namespace frame_renderer
{
    int                     n_someVar     = 1;           // scope = n
    static int              ns_someVar    = 2;           // n + static
    thread_local int        nt_someVar    = 3;           // n + thread_local
    static thread_local int nst_someVar   = 4;           // n + static thread_local
    const int               nc_someVar    = 5;           // n + const
    const volatile int      ncv_someVar   = 0;           // n + const volatile
    E_DeviceState           ne_someState  = STATE_IDLE;  // n + enum
    const E_DeviceState     nce_someState = STATE_IDLE;  // n + const + enum

    int*                    np_ptr = nullptr;            // n + pointer
    E_DeviceState*          npe_ptr = &ne_someState;     // n + pointer to enum
    E_DeviceState&          nre_ref = ne_someState;      // n + reference to enum

    extern thread_local int nxt_someVar;                 // n + extern declaration (definition is elsewhere) of thread_local variable

    int computeFrameSum(int lhs, int rhs) { return lhs + rhs; }  // function: camelCase
}

// ============================================================================
// Anonymous namespace (prefix `a`; mutually exclusive with `static`)
// ============================================================================
namespace
{
    int                  a_someVar      = 10;            // scope = a
    const int            ac_someVar     = 11;            // a + const
    E_DeviceState        ae_someState   = STATE_IDLE;    // a + enum
    int*                 ap_someVar     = &a_someVar;    // a + pointer
    const E_DeviceState& arce_someState = ae_someState;  // a + reference to const enum
}

// ============================================================================
// Free function (camelCase) demonstrating local-scope variables
// (block scope: no scope prefix; name starts at the storage slot)
// ============================================================================
void demonstrateLocals()
{
    int                 someVar      = 0;            // local (no prefix)
    static int          s_someLocal  = 0;            // local + static
    thread_local int    t_someVar    = 0;            // local + thread_local
    const int           c_someLocal  = 1;            // local + const
    E_DeviceState       e_someState  = STATE_IDLE;   // local + enum
    const E_DeviceState ce_someState = STATE_IDLE;   // local + const enum
    int*                p_dataBuffer = nullptr;      // local + pointer
    const int&          rc_someVar   = someVar;      // local + reference to const
    E_DeviceState&      re_someState = e_someState;  // local + reference to enum
}

int sendRequest(int value) { return value; }  // free function: camelCase

// ============================================================================
// Class members: access suffixes (public: none, protected: `_`, private: `__`)
// Non-static members/methods accessed via this->; static members/methods via C_Logger::...
// ============================================================================
class C_Logger
{
public:
    int         someField;        // public: no suffix
    mutable int accessCount;      // public, mutable: no suffix (mutable not encoded)
    int*        p_publicBuffer;   // public pointer member: no suffix
    static int  s_instanceCount;  // public static member (declaration)

protected:
    int            protectedField_;    // protected: suffix `_`
    E_DeviceState  e_logState_;        // protected enum member
    E_DeviceState* pe_operatingMode_;  // protected pointer-to-enum member

private:
    int           privateField__;   // private: suffix `__`
    E_DeviceState e_targetState__;  // private enum member
    static int    s_someCounter__;  // private static member

public:
    static inline thread_local int st_cache = 0;  // static thread_local member

    C_Logger()
        : someField(0), accessCount(0), p_publicBuffer(nullptr),
          protectedField_(0), e_logState_(STATE_IDLE), pe_operatingMode_(nullptr),
          privateField__(0), e_targetState__(STATE_IDLE)
    {}

    void flushBuffer()  // non-static helper method (camelCase)
    {
        this->someField = 0;
    }

    void logMessage()
    {
        this->someField++;
        this->accessCount++;
        this->protectedField_++;
        this->e_logState_ = STATE_RUNNING;
        this->pe_operatingMode_ = &this->e_logState_;
        this->privateField__++;
        this->e_targetState__ = STATE_ERROR;
        this->flushBuffer();          // non-static method call: this->method()
        C_Logger::s_instanceCount++;
        C_Logger::s_someCounter__++;
        C_Logger::resetCount();       // static method call: C_Logger::method()
    }

    void touch() const { this->accessCount++; }  // mutable modified through const method

    static int resetCount()
    {
        C_Logger::s_someCounter__ = 0;
        return C_Logger::s_instanceCount;
    }
};

// static member definitions: keyword `static` omitted; same `s_` prefixed name
int C_Logger::s_instanceCount = 0;
int C_Logger::s_someCounter__ = 0;

// ============================================================================
// Template parameters (all six kinds) and template class members
// Note: a parameter pack must be the final template-parameter of its list,
// so the three packs are demonstrated in their own declarations.
// ============================================================================
template <typename TTP_Value>                                class C_Ttp   {}; // type template parameter
template <typename... TTPP_Args>                             class C_Ttpp  {}; // type template parameter pack
template <int NTTP_Count>                                    class C_Nttp  {}; // non-type template parameter
template <auto... NTTPP_Values>                              class C_Nttpp {}; // non-type template parameter pack
template <template <typename> typename TeTP_Allocator>       class C_Tetp  {}; // template template parameter
template <template <typename...> typename... TeTPP_Policies> class C_Tetpp {}; // template template parameter pack

template <typename TTP_Value,                           // type template parameter
          int NTTP_Count,                               // non-type template parameter
          template <typename> typename TeTP_Allocator>  // template template parameter
class C_Container
{
public:
    C_Container() : value_(), e_state_(STATE_IDLE), internal__(0) {}

    TTP_Value retrieve() const { return this->value_; }

    void update()
    {
        this->value_ = TTP_Value{};
        this->e_state_ = STATE_RUNNING;
        this->internal__++;
        C_Container::s_sharedCount++;
        C_Container::s_privateTotal__++;
    }

    static inline int s_sharedCount = 0;  // public static inline member

protected:
    TTP_Value     value_;    // protected (suffix `_`)
    E_DeviceState e_state_;  // protected enum member

private:
    int               internal__;            // private (suffix `__`)
    static inline int s_privateTotal__ = 0;  // private static member (suffix `__`)
};

// ============================================================================
// Entry point exercising the runnable surface
// ============================================================================
int main()
{
    C_Logger logger;
    logger.logMessage();                // method (camelCase); internal access via this->
    logger.touch();
    logger.p_publicBuffer = nullptr;    // public field access from outside (obj.member)
    int v = C_Logger::s_instanceCount;  // static member access qualified by class name
    C_Logger::resetCount();

    C_Logger* p_logger = &logger;       // local pointer variable (block scope: p_)
    p_logger->someField = 0;            // public field access via pointer (ptr->member)

    sendRequest(0);
    frame_renderer::computeFrameSum(1, 2);
    demonstrateLocals();

    (void) v;
    
    return 0;
}
```

This example covers:

- **Anonymous namespace** variables (`a`, `ac`, `ae`, `ap`, `arce`) and the mutual exclusion of `a` with `static`.
- **cv-qualifier prefixes** (`c`, `v`, `cv`) at namespace and local scope.
- **Enum prefixes** (`e`, `ce`, `cve`) for plain-enum and enum-class variables.
- **Enumerator naming**: `UPPER_SNAKE_CASE` for plain `enum` (`STATE_IDLE`, …) and `PascalCase` for `enum class` (`DeepPurple`, …).
- **Extern declarations** (`gx`, `gxt`, `nxt`) marked as declarations only, defined elsewhere.
- **File-name convention** represented by the artifact name `ultimate_example.cpp`.
- **Function-like macro** (`SAVE_DATA()`) and **object-like macro** (`MAX_BUFFER_SIZE`).
- **Functions/methods in `camelCase`** (`sendRequest`, `computeFrameSum`, `logMessage`, `touch`, `resetCount`, `retrieve`, `update`, `main`).
- **Local (block) scope** variables with no scope prefix (`someVar`, `s_someLocal`, `p_dataBuffer`, `p_logger`, …).
- **Member access suffixes**: `public` (none), `protected` (`_`), `private` (`__`), including on pointer/enum members and static members.
- **Member access discipline**: non-static fields/methods via `this->…`; static members/methods via `C_Logger::s_…` / `C_Logger::resetCount()` / `C_Container::s_…`.
- **Namespace convention** via the `snake_case` namespace `frame_renderer`.
- **Pointer prefixes** — all 8 variants (`p`, `pc`, `pv`, `pcv`, `pe`, `pce`, `pve`, `pcve`) and the note that they apply to smart pointers alike.
- **Reference prefixes** — all 8 variants (`r`, `rc`, `rv`, `rcv`, `re`, `rce`, `rve`, `rcve`), with the cv-qualifier prefix slot intentionally omitted.
- **Scope prefixes** (`g`, `n`, `a`) and their omission at local/member scope.
- **Static linkage/storage prefixes** (`s`, `t`, `st`) at namespace scope and as class members, plus the out-of-line static-member definition pattern (keyword `static` omitted, `s_` name retained).
- **Static thread_local** namespace (`gst`, `nst`) and member (`st`) forms.
- **Type prefixes** (`C`, `S`, `E`, `U`) and **type-alias prefixes** (`TA`, `TAC`, `TAS`, `TAE`, `TAU`, `TAP`, `TAR`, `TAF`).
- **Template parameter prefixes** — all 6 kinds (`TTP`, `TTPP`, `NTTP`, `NTTPP`, `TeTP`, `TeTPP`).
- **Ultimate compound forms** (`gscvpcve_state`, `gsrcve_state`) combining scope + storage + cv + pointer/reference-to-const-volatile-enum.
- **`mutable` members** following the same naming rules as non-`mutable` members of the same access level, modifiable through a `const` method (`touch()`).
