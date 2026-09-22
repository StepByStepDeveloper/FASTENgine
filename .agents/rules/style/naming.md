# `TAPAS (C++ Naming Conventions)`

The scheme takes its name from the Spanish *tapas* — small dishes that combine into a full meal, as these small markers combine into a name — and from its own alias prefix `TAPAS` (`T`ype `A`lias `P`rotocol `A`bstract `S`truct).

## `Scope and permitted deviations`

Every entity created in this project is named by the rules of this document — an entity the sections below do not name (a label, a module name, a concept) is not constrained by them. When a name is ours to choose, these conventions win; the two situations that may override a rule are:

- the name is fixed by the language or by an existing system / third-party interface — `main`, constructors, destructors, conversion operators, `operator+`, and an override that has to keep the library's name (e.g. `std::exception::what()`);
- the entity is legacy code, carries established terminology, or has to be named so that it unifies with third-party code it is used together with — there the accepted name may be kept as it stands (a vendor method name kept so that the two hierarchies stay interchangeable, `dot()` / `cross()` kept because that is what the operations are called).

A deviation covers only the name that is forced; everything else about the entity keeps the conventions — the type keeps its prefix (§1.2.1), a pointer to it keeps its marker (§1.1), the file keeps its `snake_case.cpp` name, the namespace keeps its `snake_case` name. When the forced name is not self-evident, the declaration carries a comment that names the reason (`// Deviation: the name is fixed by std::exception`).

Every code fragment in this document is written to compile as C++17; where a rule's prose names a C++20 form (a `requires`-clause, a concept), that form is an optional refinement of the same rule rather than a requirement of the conventions. This document decides names and the form in which a member is reached (§5, §8); how the code is otherwise formatted and documented lies outside its scope.

Fragments that exist only to show a naming form declare names nothing reads, so a build that enables the unused-declaration warnings (`-Wunused-variable` and `-Wunused-function`; Clang adds `-Wunused-const-variable` and `-Wunused-private-field`) reports those declarations; no fragment in this document produces a compiler error. The fragments below illustrate names rather than the program itself: their `//` comments annotate the name rather than document the declaration, and the fragments are laid out by hand for reading.

***Example***:

```C++
#include <exception>

class C_FileError final : public std::exception   // C_ prefix: convention
{
public:
    const char* what() const noexcept override;   // Deviation: the name is fixed by std::exception
    int retrieveErrorCode() const;                // our own method: imperative verb (§5), no deviation

private:
    int priv_errorCode;                           // member: access marker only (§8); no marker block, no deviation
};
```

- `C_FileError` — the type keeps its `C_` prefix: the deviation applies to `what()` alone.
- `what()` — the only name in the class that does not follow these conventions; the comment states why.
- `retrieveErrorCode()` — a method of the same class: imperative verb (the name starts with a verb; §5), so the rule applies and nothing is deviated (`errorCode()` would be a noun, and nouns belong to variables; §1.1).
- `priv`\_`errorCode` — a field of the same class: a noun with the leading access marker (`pub_`, `prot_` or `priv_`; §8) and no marker block (an ordinary `int` field has nothing to mark; §1.1), again with no deviation.

## `Organization of this document`

The rules are layered, and this is the order they expect to be read in:

- **Marker grammar — §1.** What a marker family is, which markers exist, in what order they concatenate, and what each letter means: `1.1` variables, `1.2` types, `1.3` template parameters. No later section adds a marker to this grammar; the one family defined outside it is the member's leading **access marker** (`pub_`, `prot_` or `priv_`), introduced in [Member variable naming conventions](#8-member-variable-naming-conventions).
- **One table per entity — §2 to §9.** Each table names an entity and the style-form it has to follow; the style-forms themselves are defined in §1.
- **One worked example — §10.** A single translation unit that exercises the rules above; the coverage list at its end names the few it points at instead of demonstrating.

A reader who is here to name things rather than to read the document through needs less: §1.1 with §7 and §8 covers a variable, §1.2.1 with §4 a type (§1.2.3 an alias), and §5 a function; §1.2.2 is the reference for deciding a type's role. Every other entity has its own table — §2 a file, §3 a namespace, §6 a macro or enumerator, §9 a template parameter — and §10 shows the rules in one file.

A variable is the one entity whose rules are spread over the places below — one per scope it can be declared in, plus the style-form table its own section carries; this table says where to look instead of repeating the grammar:

| Variable scope                               | Where its rules are                                                                                            | Examples                                           |
|:-------------------------------------------- |:-------------------------------------------------------------------------------------------------------------- |:-------------------------------------------------- |
| Namespace (`g`lobal / `n`amed / `a`nonymous) | [Variable markers](#11-variable-markers) and [Scope markers](#111-scope-markers)                               | `someVar`\_`g`, `someVar`\_`ns`, `someVar`\_`a`    |
| Block (function or block)                    | The *local (function/block) scope* and *function parameters* notices under [Scope markers](#111-scope-markers) | `someVar`, `someVar`\_`s`, `dataBuffer`\_`p`       |
| Class member                                 | [Member variable naming conventions](#8-member-variable-naming-conventions)                                    | `pub`\_`accessCount`, `priv`\_`targetState`\_`e`   |

The style-forms themselves are tabulated in [Non-Member variable naming conventions](#7-non-member-variable-naming-conventions) for a variable that is not a member — the minimal rendering shown there (no [`scope`] marker) is valid at block scope only — and in [Member variable naming conventions](#8-member-variable-naming-conventions) for a member.

## `1. Identifier markers`

In this document, a name in square brackets is a **marker family** — the position into which the rules write whichever marker of that family applies (`[`scope`]` for `g` / `n` / `a`, `[`type-prefix`]` for `C_` / `IS_` / `PAC_` and the rest), never a literal token; whether a position may stay empty is stated by the rules of the section that defines the style-form. A *style-form* is a written shape a name has to follow — the casing plus the markers or prefixes that shape prescribes. The tables of the later sections name the style-form they require, either one defined here (`normal-var`, `enum-var`, `type-name` and the rest), a casing of their own (`snake_case.cpp` for a file), or a prefix this document defines written together with a casing (`TTP_PascalCase` for a template parameter).

### `1.1. Variable markers`

A variable name is a **base name** followed by a **marker block**. The base name is a meaningful noun in `camelCase` — a predicate, for a `bool` (see the Boolean notice below) — and the block is every marker that applies to the variable, written as lowercase letters after a single `_`, in the fixed order below (each marker listed below appears at most once, in the specified order).

- `normal-var` (non-enum and non-pointer and non-reference) variable: `camelCase`\_[`scope`][`storage-class`][`cv-qualifier`]
- `enum-var` variable: `camelCase`\_[`scope`][`storage-class`][`cv-qualifier`][`enum`]
- `pointer-var` variable: `camelCase`\_[`scope`][`storage-class`][`cv-qualifier`][`pointer`]
- `reference-var` variable: `camelCase`\_[`scope`][`storage-class`][`reference`]

The four forms differ in their **kind marker** — the marker that says what kind the variable is: `[`enum`]`, `[`pointer`]` or `[`reference`]`, with no kind marker at all for `normal-var`. A variable carries at most one of them, because each kind marker already encodes what its type designates (a pointer to an enum object is `pe`, never `ep`; a reference to an enum object is `re`), and it is the last position of the block.

*Placeholders*: the names used in the examples of this document (`someVar`, `var_g`, `ptr_np`, `SomeType`, and the type-shaped placeholders `C_X`, `PC_X<C_A>` and `C_Derived`) show the shape of a name, not the name of anything real; a name written in code states what the entity holds. A fragment may also name an entity the ultimate example declares, such as `S_Point` or `intTarget_g`, when the sentence is about the marker rather than about the entity.

**Important notice for Boolean variables**:

> A `bool` variable is the one variable whose base name is not a noun: it is named by a **predicate** — `is`, `has`, `can`, `needs` or another verb of the same kind, immediately followed, in `camelCase`, by the noun or adjective the predicate is about — so that the name reads as the question the variable answers (`isVisible`, `priv`\_`isDirty`, `hasFinished`\_`c`). The marker block is untouched: a predicate takes the same trailing block any other base name takes (`hasFinished`\_`c`, `isInitialized`\_`a`). A method that answers the same question follows the function style-form, `isVisible()` / `hasError()` (see [Function-like Macro and Function/Method naming conventions](#5-function-like-macro-and-functionmethod-naming-conventions)).

The marker block is trailing on purpose: the meaningful part of every name comes first, so a reader (and an editor's completion list) sees *what the variable holds* before *how it is qualified*, and no reading order is inverted. The member's leading **access marker** is the one deliberate prefix in the scheme: a member announces itself as a member before its base name is read (see [Member variable naming conventions](#8-member-variable-naming-conventions)). A trailing marker block also cannot produce a reserved identifier: the `camelCase` base name leads the name, so no underscore opens it, and the block never puts two underscores in a row.

**Important notice for an absent marker block**:

> A variable to which no marker applies (an ordinary local) is written `someVar`, **never** `someVar`\_. The separating underscore exists only to introduce a non-empty marker block.

**Important notice for references**:

> Unlike pointers, references in C++ cannot carry cv-qualifiers (const, volatile) themselves. Therefore, the [`cv-qualifier`] marker is intentionally omitted from the reference variable naming formula. The cv-qualifiers of the referenced object are fully captured by the [`reference`] marker (e.g., `rc` for `reference to const`, `rcv` for `reference to const volatile`). The [`cv-qualifier`] marker is never written together with the [`reference`] marker.

**Important notice for cv-qualifiers inside the `pointer` and `reference` markers**:

> The letters of a [`pointer`] or [`reference`] marker describe the *pointed-to* / *referred-to* type, not the variable's own type: `pcve` is a `pointer` to an object of `const volatile` `enum` type. A cv-qualified variable of such a type therefore carries cv letters in two different markers — `someVar`\_`gcpc` is a `const` pointer to a `const` object, while `someVar`\_`gpc` is a non-`const` pointer to a `const` object. The order of the markers separates the two readings: the variable's own [`cv-qualifier`] always precedes the kind marker, and the cv-qualifiers of the pointed-to / referred-to type are always inside it.

#### `1.1.1. Scope markers`

- `g`: variable in `global` namespace (`g` - `g`lobal)
- `n`: variable in `named` namespace (`n` - `n`amed)
- `a`: variable in `anonymous` (unnamed) namespace (`a` - `a`nonymous)

***Example 1***: `someVar`\_`g` - variable in the `global` namespace with name `someVar`

***Example 2***: `someVar`\_`n` - variable in the `named` namespace with name `someVar`

***Example 3***: `someVar`\_`a` - variable in the `anonymous` namespace with name `someVar`

**Important notice for the `a` marker**:

> Variables declared inside an anonymous (unnamed) namespace have internal linkage by definition — the compiler guarantees this automatically, so there is no need for the `static` (`s`) storage-class marker, and these conventions forbid it. The `a` marker is therefore mutually exclusive with the `static` (`s`) and `extern` (`x`) storage-class markers (see the storage-class markers below). An anonymous-namespace variable with internal-linkage storage is written `someVar`\_`a`, never `someVar`\_`as`. The `a` marker combines with `thread_local` in the ordinary way, because that keyword changes duration rather than linkage: `someVar`\_`at`, `someVar`\_`atc`. It combines with no linkage keyword: `someVar`\_`as`, `someVar`\_`ast`, `someVar`\_`ax` and `someVar`\_`axt` are not names this document defines.

**Important notice for local (function/block) scope**:

> Variables declared inside a function or block scope are *block-scoped*: they have no linkage and are not members of any namespace. They intentionally **omit the [`scope`] marker** entirely — `g`, `n` and `a` describe namespace scope only, so no name of a local variable ever carries one. The marker block of a local variable therefore starts at the [`storage-class`] position (e.g., a `static` local is `someVar`\_`s`, a `thread_local` local is `someVar`\_`t`, a `const` local is `someVar`\_`c`), and a local that has nothing to mark at all is written with no marker block and no trailing underscore (e.g., `someVar`). A name introduced by a structured binding (`auto [xCoordinate, yCoordinate] = S_Point{1, 2};`) is a block-scope name as well, but it binds to a subobject instead of declaring a variable of its own, so it carries no marker block and no separating underscore. The minimal forms shown in the [Non-Member variable naming conventions](#7-non-member-variable-naming-conventions) table (such as `operatingMode`\_`e`, `dataBuffer`\_`p`) are valid only at local scope.

**Important notice for function parameters**:

> A function parameter is block-scoped exactly like any other local variable, so it omits the [`scope`] marker; and because `static` and `extern` cannot be applied to a parameter, no [`storage-class`] marker can appear on one either. What remains is the [`cv-qualifier`] and kind part of the block, so a pointer parameter is `vertices`\_`p` — the marker trails the name, it never precedes it — while an unqualified one keeps its bare name (`vertexCount`).

#### `1.1.2. Storage-class markers`

- `s`: `static` variable (`s` - `s`tatic)
- `t`: `thread_local` variable (`t` - `t`hread_local)
- `st`: `static` `thread_local` variable (`st` - `s`tatic `t`hread_local)
- `x`: `extern` variable (`x` - e`x`tern)
- `xt`: `extern` `thread_local` variable (`xt` - e`x`tern `t`hread_local)

***Example***: `someVar`\_`st` - `static` `thread_local` variable with name `someVar`

**Important notice for the `s` marker at namespace scope**:

> Every namespace-scope variable has static storage duration, so the `s` marker does not record that. It records the `static` keyword itself: the variable is visible only within its own translation unit (e.g., `someVar`\_`gs` or `someVar`\_`ns`) — a distinction that matters in a project with many source files. The same reasoning applies to both the `global` (`g`) and the `named` (`n`) scope markers. The marker records the keyword written in the declaration, not the linkage the variable ends up with: a namespace-scope `const` object that is not `volatile` already has internal linkage without any marker, while a `const volatile` one keeps external linkage. On a class member the same letter reads as class-level shared storage and says nothing about linkage — the member notice in [Member variable naming conventions](#8-member-variable-naming-conventions) explains the difference. `inline` is not a keyword the markers name either: a namespace-scope `inline` variable keeps its plain [`scope`] marker, while an `inline static` member keeps its `s` (see `C_Container`::`pub`\_`sharedCount`\_`s` in §10).

**Important notice for the `x` marker**:

> The `x` marker marks a variable that is *declared* in one translation unit and *defined* in another one. The `extern` keyword belongs to that declaration only, and the name does not change: a variable has exactly one name, so the definition is written with the same marked name (`extern int someVar_gx;` declares it; `int someVar_gx = 42;` defines it). `s` and `x` never combine in one name: the two keywords state opposite intents — an entity its own translation unit keeps, and an entity another translation unit has to provide — and a name records the one its declaration carries. A `static` declaration followed by an `extern` redeclaration of the same name is still accepted in its own translation unit — the redeclaration inherits the internal linkage of the first one — and the failure surfaces at link time, in a translation unit that expects a definition no one provides. The `xt` marker is the `thread_local` counterpart and follows the same rule.

***Example 1***: `someVar`\_`gx` - `extern` variable in a `global` namespace with name `someVar` (e.g. declared in this translation unit, defined elsewhere)

***Example 2***: `someVar`\_`nxt` - `extern` `thread_local` variable in a `named` namespace with name `someVar`

#### `1.1.3. CV-qualifier markers`

- `c`: `const`-like variable — `const`, `constexpr` (`c` - `c`onst)
- `v`: `volatile` variable (`v` - `v`olatile)
- `cv`: `const` `volatile` variable (`cv` - `c`onst `v`olatile)

***Example***: `someVar`\_`cv` - `const` `volatile` variable with name `someVar`

**Important notice for `const`-like declarations**:

> Every declaration that gives a variable a `const`-qualified type carries the `c` marker, whichever keyword produced that type: `const` and `constexpr` are the same case, because for an object declaration `constexpr` implies `const` already. The marker keeps its usual position: a `constexpr` local is `someConstVar`\_`c`, a `static constexpr` local is `someConstVar`\_`sc`, a `constexpr` variable at `global` namespace scope is `someConstVar`\_`gc`, and a `global` `static constexpr` one is `someConstVar`\_`gsc`. `constexpr` is not the `static` keyword, so it never adds the `s` [`storage-class`] marker on its own — `s` still tracks an explicit `static`. At member scope the same letters follow the access marker and the base name (see [Member variable naming conventions](#8-member-variable-naming-conventions)): a `static constexpr` member is `pub`\_`someConstVar`\_`sc`, a `const` member is `pub`\_`someConstVar`\_`c`. A reference is the declaration where `constexpr` adds no `c` marker: `constexpr int& someVar`\_`gr = intTarget`\_`g;` gives the variable no `const`-qualified type — the keyword asks for a constant-initialized reference, not a `const` referent, and the object it names stays modifiable — so the name keeps the plain [`reference`] marker (see [Reference markers](#116-reference-markers)).

**Important notice for what the `c` marker does not cover**:

> Two keywords carry `const` in their name without making a variable `const`, so neither adds the `c` marker: `consteval` describes a function, and functions are named by the [Function-like Macro and Function/Method naming conventions](#5-function-like-macro-and-functionmethod-naming-conventions) without a marker; `constinit` demands constant initialization only — the object it declares stays modifiable — so such a variable keeps its ordinary name. Constants that are not variables are the other exception: an object-like macro and an enumerator carry no marker at all and are named by the [Object-like Macro and Enumerator naming conventions](#6-object-like-macro-and-enumerator-naming-conventions).

#### `1.1.4. Enum markers`

- `e`: variable of `enum` or `enum class` type (`e` - `e`num)

***Example***: `someVar`\_`e` - variable of `enum` (or `enum class`) type with name `someVar`

**Rationale for the enum marker**:

> The `e` marker on a variable (e.g., `varName`\_`e`) makes it possible to recognize that the variable is an enumeration. This is especially important when the variable is of a plain `enum` (not `enum class`), because plain enumerators can be assigned directly as `VAL` instead of `E_EnumType::VAL`. If a reader sees `var = VAL`, they might not realize the variable is an enumeration, because in that representation `VAL` may be taken for some constant rather than an enumerator. The `e` marker (`var_e = VAL`) solves that problem. The marker describes the variable's own kind, so a variable whose type merely holds enumerators — a container of them, a class with an enumerator member — does not receive it and is written as a `normal-var`; the notice in [Reference markers](#116-reference-markers) lists the two kinds of variable that take no kind marker at all.

#### `1.1.5. Pointer markers`

- `p`: `pointer` to an object or a function of any type, or to `void` (`p` - `p`ointer)
- `pc`: `pointer` to an object of `const` type (`pc` - `p`ointer `c`onst)
- `pv`: `pointer` to an object of `volatile` type (`pv` - `p`ointer `v`olatile)
- `pcv`: `pointer` to an object of `const` `volatile` type (`pcv` - `p`ointer `c`onst `v`olatile)
- `pe`: `pointer` to an object of `enum` (or `enum class`) type (`pe` - `p`ointer `e`num)
- `pce`: `pointer` to an object of `const` `enum` (or `enum class`) type (`pce` - `p`ointer `c`onst `e`num)
- `pve`: `pointer` to an object of `volatile` `enum` (or `enum class`) type (`pve` - `p`ointer `v`olatile `e`num)
- `pcve`: `pointer` to an object of `const` `volatile` `enum` (or `enum class`) type (`pcve` - `p`ointer `c`onst `v`olatile `e`num)

**Important notice for the `pointer` markers**:

> The pointer markers are applicable to smart pointers as well: the marker records that the variable *designates* an object instead of holding it, so a `std::unique_ptr<C_SomeType>` variable is a pointer variable (`someVar_gp`) even though its own type is a class.

***Example***: `someVar`\_`pcve` - `pointer to an object of const-volatile-enum type` with name `someVar`

#### `1.1.6. Reference markers`

- `r`: `reference` to an object or a function of any type (`r` - `r`eference)
- `rc`: `reference` to an object of `const` type (`rc` - `r`eference `c`onst)
- `rv`: `reference` to an object of `volatile` type (`rv` - `r`eference `v`olatile)
- `rcv`: `reference` to an object of `const` `volatile` type (`rcv` - `r`eference `c`onst `v`olatile)
- `re`: `reference` to an object of `enum` (or `enum class`) type (`re` - `r`eference `e`num)
- `rce`: `reference` to an object of `const` `enum` (or `enum class`) type (`rce` - `r`eference `c`onst `e`num)
- `rve`: `reference` to an object of `volatile` `enum` (or `enum class`) type (`rve` - `r`eference `v`olatile `e`num)
- `rcve`: `reference` to an object of `const` `volatile` `enum` (or `enum class`) type (`rcve` - `r`eference `c`onst `v`olatile `e`num)

***Example***: `someVar`\_`rcve` - `reference to an object of const-volatile-enum type` with name `someVar`

**Important notice for the designated type**:

> The designated type may itself be a `pointer`, an array or a function: the marker names the outermost kind only, and its letters describe the cv-qualification and the enum-ness of what that outermost kind designates — one level down, never the full shape of the type. A pointer to a pointer (`int**`) is therefore `someVar`\_`gp`, a pointer to a function (`int (*)(int)`) is `someVar`\_`gp`, a pointer to an array (`char (*)[4]`) is `someVar`\_`gp`, and a reference to a pointer (`int*&`) is `someVar`\_`gr`. Qualification deeper than that one level is not encoded: `int* const*` is `someVar`\_`gpc`, because the type it designates (`int* const`) is itself cv-qualified, while `const int**` is `someVar`\_`gp`, because the type it designates (`const int*`) is a pointer rather than a cv-qualified type and the `const` it points to lies one level further down — the letters never describe the pointee of a pointee. A function type carries no cv-qualifiers — a qualifier written on top of one is ignored — so the `c` and `v` letters never describe a function: a pointer to a function carries them either for itself, before the kind marker (`int (* const someVar`\_`gcp)(int)`), or for a pointer it designates (`int (* const * someVar`\_`gpc)(int)`). The value category is not encoded: an rvalue reference takes the same marker as any other reference (`int&&` is `someVar`\_`gr`, `const int&&` is `someVar`\_`grc`). Two kinds of variable take no kind marker at all and are written as `normal-var`: a raw array (`char buffer`\_`g`\[4\]) — an array is not a `pointer` — and a pointer to a member (`int C_X::* offset`\_`g`), whether it designates a member object or a member function, because it designates a member rather than an object.

#### `1.1.7. Compound marker examples`

***Example 1***:

```C++
enum E_DeviceState { STATE_IDLE, STATE_RUNNING, STATE_ERROR };

const volatile E_DeviceState targetState_gcve = STATE_IDLE;

static const volatile E_DeviceState* const volatile state_gscvpcve = &targetState_gcve;
```

Variable `state`\_`gscvpcve` is `global`-scope, internal-linkage (`static`), `const volatile` pointer to an object of `const-volatile-enum` type, with name `state` (`g`lobal `s`tatic `c`onst `v`olatile `p`ointer `c`onst `v`olatile `e`num):

- variable has `global` scope
- variable has internal linkage (`static`)
- variable has `const volatile` qualifiers
- variable has `pointer` type
- variable points to an object of `const-volatile-enum` type, specifically `E_DeviceState`

***Example 2***:

```C++
enum E_DeviceState { STATE_IDLE, STATE_RUNNING, STATE_ERROR };

const volatile E_DeviceState targetState_gcve = STATE_IDLE;

static const volatile E_DeviceState& state_gsrcve = targetState_gcve;
```

Variable `state`\_`gsrcve` is `global`-scope, internal-linkage (`static`) reference to an object of `const-volatile-enum` type, with name `state` (`g`lobal `s`tatic `r`eference `c`onst `v`olatile `e`num):

- variable has `global` scope
- variable has internal linkage (`static`)
- variable has `reference` type
- variable refers to an object of `const-volatile-enum` type, specifically `E_DeviceState`

### `1.2. Types`

Possible type cases:

- `type-name`: [`type-prefix`]_`SomeType`
- `type-alias-name`: [`type-alias-prefix`]_`SomeType`

#### `1.2.1. Type prefixes`

A type prefix consists of optional `role markers` followed by a `type letter`.

`Type letters`:

- `C`: `class` (`C` - `C`lass)
- `S`: `struct` (`S` - `S`truct)
- `E`: `enum` or `enum class` (`E` - `E`num)
- `U`: `union` (`U` - `U`nion)

`Role markers` (normative clauses in [Abstraction & protocol markers](#122-abstraction--protocol-markers); the lines below are a summary only):

- *(none)*: concrete type
- `I`: `interface` type — a complete dynamic contract: pure virtual functions only, no data member, destruction through the base is well-defined or impossible to write (`I` - `I`nterface)
- `A`: `abstract` type — a base that is not yet complete: abstract, yet failing at least one `I` clause — typically it carries state or implementation (`A` - `A`bstract)
- `P`: `protocol` type — a compile-time contract on a statically known derived type: a class template that states what the class deriving from it owes (`P` - `P`rotocol)

`Role markers` concatenate in the fixed order (`P` must be before `A`) and admit exactly five combinations: *(none)*, `I`, `A`, `P`, `PA` (`PI` and `IA` cannot be written — see the composition rules below).

Resulting prefixes: `C`, `S`, `E`, `U`, `IC`, `IS`, `AC`, `AS`, `PC`, `PS`, `PAC`, `PAS`.

**Important notice for `union` and `enum`**:

> `Role markers` never combine with the `U`/`E` `type letters` — unions cannot declare virtual member functions or participate in inheritance, and an enum declares nothing but its enumerators: no data members and no virtual functions.

***Example 1***:

```C++
enum class E_SomeType { Enum1, Enum2 };

const E_SomeType someVar_gce = E_SomeType::Enum1;
```

- `E_SomeType`: An `enum class` type with name `SomeType`
- `someVar`\_`gce`: A `global const enum` variable (instance) of `enum class` type (`E_SomeType`), marked with the `enum` marker (`e`)

***Example 2***:

```C++
class C_SomeType {};

C_SomeType var_g;

const C_SomeType* someVar_gpc = &var_g;
```

- `C_SomeType`: A `class` type with name `SomeType`
- `var`\_`g`: A `global` variable (instance) of `class` type (`C_SomeType`)
- `someVar`\_`gpc`: A `global pointer to const` object of `class` type (`C_SomeType`), marked with the `pointer-to-const` variant of the `pointer` marker (`pc`)

***Example 3***:

```C++
struct S_SomeType {};

S_SomeType var_g;

const S_SomeType& someVar_grc = var_g;
```

- `S_SomeType`: A `struct` type with name `SomeType`
- `var`\_`g`: A `global` variable (instance) of `struct` type (`S_SomeType`)
- `someVar`\_`grc`: A `global reference to const` object of `struct` type (`S_SomeType`), marked with the `reference-to-const` variant of the `reference` marker (`rc`)

#### `1.2.2. Abstraction & protocol markers`

The summary above is enough to write a prefix: the clauses below are what decides a type's role, with the algorithm that applies them.

Terms used below:

- **declared by the type** — written in the type's own definition; **inherited** — brought in with a base class; together they form the type's **member set**. Implicitly-declared special member functions are neither: they appear in no definition, so they never satisfy a clause. `I6` is the exception — it reads the **effective destructor** (the one the type ends up with, declared or implicitly declared), because that is what a `delete` through the type actually runs.
- **special member function** — default constructor, copy/move constructor, copy/move assignment operator, destructor, in any form (defaulted, deleted, pure).
- **data member** — a non-static data member; static data members are not fields and carry no per-object state.
- **handle** — a pointer or a reference through which a user reaches an object.
- **contract member** — a member function (declared by the type) that requires something of the class deriving from the template — the static counterpart of an interface's pure virtual function. It reaches that class through `TTP_Derived`, the fixed name this document requires for the template parameter that stands for it (see [Template parameter naming conventions](#9-template-parameter-naming-conventions)). It is one of three forms — a non-static member function, a static member function or a member function template — for example `void refresh() { static_cast<TTP_Derived&>(*this).refreshState(); }`, which requires the deriving class to provide `refreshState()`. Where the member's text stands does not matter: a declaration, a trailing return type, a body written in the class and a definition written outside it all state the same requirement.
- **mixin** — a class template that hands functionality to the class deriving from it (its **host**), typically through CRTP; the member a contract member calls on that host is the mixin's **hook**; a **protocol** is this document's name for the mixin form that obliges its host (see `P` below).
- **abstract** — standard C++ sense: at least one pure virtual function in the member set has no final overrider in the type (`std::is_abstract_v<T>`); otherwise the type is **concrete**.

`Role markers`:

- **`I` (interface)** — a complete dynamic contract:
  1. the type is abstract;
  2. it declares or inherits at least one pure virtual non-special member function;
  3. every non-special member function in its member set is pure virtual;
  4. it declares no contract member;
  5. it has no data member;
  6. destroying an object through the interface is well-defined. Only two destructor forms qualify: a `public` `virtual` destructor, so that `delete` through the interface runs the whole destruction chain, or a destructor that is not `public` (`protected` or `private`, `virtual` or not), so that `delete` through the interface cannot be written at all. The single forbidden form is a `public` non-`virtual` destructor that is not deleted — declared or implicitly declared — where `delete` through the interface compiles, runs only the base part of the chain and leaves the derived type's own destructor unrun, which is undefined behavior; a deleted destructor is safe rather than forbidden, because deleting through it does not compile;
  7. static members are permitted and lie outside `I2`, `I3` and `I5`.

  *Consequences*: an interface inherits only from interfaces (`I3`, `I5` and `I6` keep an implementation, a data member and an unsafe destructor out; a base whose only failing clause is `I2` — its single pure virtual function is a special member — is the one exception) — which admits the *composite* form, an interface that aggregates several contracts and declares nothing of its own (it passes `I2` on what it inherits) — and no helper implementation may be added to one: helpers belong to an abstract type. Clause `I4` is not a matter of taste: a user holding the interface sees exactly its virtual functions, so a member that is not virtual is not part of the contract at all, and an obligation toward a derived type is never visible through the interface.
- **`A` (abstract)** — an incomplete base that exists to be completed:
  1. it is abstract;
  2. it fails at least one `I` clause — that is what distinguishes it from an interface. Any of `I2`, `I3`, `I5` or `I6` can be the failing one: most often `I5` (it carries a data member, that is the state its derived types share) or `I3` (it carries an implementation), occasionally `I2` (its member set holds no pure virtual non-special member function — the only pure virtual function in its member set is a special member such as a destructor) or `I6` (an unsafe destructor). `I1` holds by definition and `I7` only permits, so neither can fail; `I4` cannot be the failing clause here either — it fails exactly when the type declares a contract member, and clause `A3` below requires a type marked `A` to declare none, so that type is `PA`, never `A`; a type that fails none of `I1`–`I7` is an interface itself;
  3. it declares no contract member (a contract member makes it `PA`);
  4. it may still declare pure virtual functions of its own, `override = 0` re-declarations, data members and implementations; whether objects are destroyed through it is left to the destruction rule below.
- **`P` (protocol)** — a compile-time contract on a statically known derived type:
  1. it declares at least one contract member (the derived type passes itself as `TTP_Derived`);
  2. everything else is optional: data members, static members, non-virtual implementations and virtual members are all allowed;
  3. the marker states what the type *requires* of its derived type, not what it *implements* itself: whether a protocol carries a vtable is visible from its declarations, not from its name. A protocol is the contract side of a **mixin** (see *Protocol and mixin* below), and a protocol that also implements a dynamic contract is a **mixin over an interface**, named by these same clauses (`PC_`/`PAC_`); the Guidance below still recommends decomposing it into a dynamic base plus a standalone protocol.

Contract forms:

- An `I` type states a **dynamic** contract: everything a user may do with an object is reachable through the type itself, so every member of the contract is virtual, and the implementor's obligation is to override every pure virtual function — a derived type that leaves one unoverridden stays abstract.
- A `P` type states a **static** contract: the obligations are the members named by its contract members, and they are visible to the compiler only, never through the type — a protocol offers no polymorphic handle: it is reached statically, and `PC_X<C_A>` and `PC_X<C_B>` are unrelated types.
- Both markers oblige a derived type; they differ in the form of the contract and in what the type gives its users: an interface is reached through a handle, a protocol only statically. An `A` type states no contract of its own.

Composition rules:

- `Role markers` concatenate in the fixed order (`P` must be before `A`). Exactly five marker combinations exist: *(none)*, `I`, `A`, `P`, `PA`.
- **`I` and `P` are mutually exclusive by clause, not by argument**: `P` requires a contract member (clause `P1`), and an interface is forbidden to declare one (clause `I4`) — `PI` cannot be written. **`I` and `A` are alternatives, not composable roles**: `A` is defined as failing at least one `I` clause (clause `A2`), so a type satisfying every `I` clause is an interface itself and the `I` marker leaves `A` nothing to add.
- **`PA` (`PAC_`, `PAS_`)** is the only hybrid: a protocol that is abstract. Its abstractness may come from a pure virtual function it declares itself or from an inherited pure virtual function it does not override.
- One type bears exactly one resulting prefix; no other combinations exist.

Mechanical classification algorithm:

1. Does the type declare a contract member (a member function whose declaration or definition names `TTP_Derived`)? If any exist, remember marker `P`.
2. Is the type abstract in the standard C++ sense — at least one pure virtual function (declared by the type or inherited) has no final overrider in it?
   - No → the type is concrete: `PC_`/`PS_` if marker `P` was remembered, otherwise `C_`/`S_`. Implementing every inherited pure virtual function makes a type concrete even though it keeps a vtable (e.g. `C_Button final : public AC_WidgetBase`).
   - Yes → `PAC_`/`PAS_` if marker `P` was remembered (a contract member already breaks clause `I4`, and the remembered `P` settles the role, so there is nothing left to ask); otherwise continue.
3. Are the remaining `I` clauses (`I2`, `I3`, `I5` and `I6` — `I1` and `I4` are settled by the two steps above; `I7` merely permits static members and cannot fail) satisfied?
   - Yes → `IC_`/`IS_`.
   - No → `AC_`/`AS_`.

Additional rules:

- **When an obligation is checked** — an interface's obligation is checked wherever the type is used: a derived type that leaves any pure virtual function unoverridden stays abstract, so the first attempt to create an object fails. A protocol's obligation is checked where the contract member is instantiated, i.e. at its first use: a protocol whose contract member is never used checks nothing, and a type that violates it can be declared, instantiated and run. To check a protocol early, either make the contract member virtual (the diagnostic then arrives at the first use of the derived type that needs its vtable — an object creation, or a virtual member the derived type defines out of line — instead of at the first call of the contract member), or assert the obligation outside the protocol once the derived type is complete (`static_assert(requires (C_Derived& derived_r) { derived_r.refreshState(); });`), or constrain the point of use with a concept. A `static_assert` inside the protocol's own body does not work: the derived type is still incomplete there, so the assertion fails even for a derived type that provides everything.
- **Destruction rule** — a base class is the only handle the user of a hierarchy holds, so every base is a potential deletion site, and deletion is the one operation whose mistake is silent: with a `public` non-`virtual` destructor, `delete` through a pointer or reference to the base compiles, runs the destruction chain as if the object were of the base's own type — the derived type's destructor never runs — and asks for a deallocation of the base's size although the derived object was allocated with its own, which the standard calls undefined behavior (in practice: the derived part is left un-destroyed and the heap can be corrupted). The rule therefore lets the base's own declaration settle the question once, so that deleting through a base is always either well-defined or impossible to write:
  - a base through which objects are owned declares a **`public` `virtual` destructor** — declared, or implicitly declared as `virtual` by the language (`IS_Drawable` in the example below);
  - a base that declares no virtual function at all is never owned through, so it closes ownership off with a **destructor that is not `public`** — `protected` (or `private`) and non-`virtual`, so that deleting through a pointer or reference to it cannot be written at all and the mistake becomes a compile error instead of undefined behavior (`PC_Refreshable` in the example below); a base that carries virtual functions needs no closure — its `public` `virtual` destructor, declared or inherited from the interface (`PC_DrawMixin` in §10), already makes deletion through it well-defined. A `protected virtual` destructor satisfies clause `I6` just as well and is equally safe; the non-`virtual` form is the one this document expects for such a base, because a base that is never owned needs no vtable entry for its destructor;
  - a **`public` non-`virtual` destructor that is not deleted, on a type with virtual functions** is therefore a defect — it is exactly the form that permits the undefined deletion. An explicitly deleted destructor is not this case, even though both GCC and Clang name the declaration in `-Wnon-virtual-dtor`: deleting through it does not compile, so there is no undefined deletion to permit. Both GCC and Clang diagnose the declaration (`-Wnon-virtual-dtor`); the delete site itself is diagnosed as well (`-Wdelete-non-virtual-dtor`, accepted by both GCC and Clang; Clang prints it under `-Wdelete-non-abstract-non-virtual-dtor` for a non-abstract base and under `-Wdelete-abstract-non-virtual-dtor` for an abstract one). `-Wall` enables the delete-site diagnostic but not the declaration one, so a project that wants to hear about the declaration names `-Wnon-virtual-dtor` itself.

  *Ownership, not dispatch*: the rule asks what happens to the type, not how it dispatches. Whether a type carries a vtable is visible from its declarations, never from its marker, so a `P` type that happens to be polymorphic — a mixin over an interface such as `PC_DrawMixin` — follows the rule like any other base, while a mixin that is never owned through its base form declares the protected non-virtual destructor even though it declares no virtual function at all: ownership is closed off by the rule, and closing it costs nothing here.
- **Template rule** — an ordinary class decides its role once and the name records that decision; a class template is a family of types instead, and whether an instantiation is abstract, declares a contract member or carries a data member can depend on its arguments. A wrapper that inherits its own parameter — `template <typename TTP_Base> class C_Wrapper : TTP_Base {};` — is abstract for `TTP_Base` = `IS_Drawable` and concrete for `TTP_Base` = `C_Line`, so one and the same name would promise a concrete type to one user and an incomplete base to another. A name cannot carry two roles, so the rule fixes the role at the primary definition and demands that every accepted argument preserve it:
  - the marker is chosen from the **primary definition** — a specialization that would change the role breaks the rule, because the name would then be read differently depending on the argument list;
  - a template whose role varies with its arguments must be **constrained** so that only arguments preserving the role are accepted — a `requires`-clause (`requires (!std::is_abstract_v<TTP_Base>)`), a concept, or a `static_assert` in the body; the constraint has to *reject* the offending arguments, not merely warn about them.

  *CRTP parameters are the safe case*: `TTP_Derived` is never used as a base — it appears only inside the protocol's own members (`static_cast<TTP_Derived&>(*this).refreshState();`) — so `PC_Refreshable` and `PC_DrawMixin` bear the same role for every derived type, and a protocol can be named `PC_` without asking what it will be instantiated with.
- **Protocol and mixin** — a protocol *is* a mixin: the class template hands functionality to the class deriving from it (typically through CRTP) and, by the members its contract members call, states what that class owes back. `P` types are therefore a proper subset of mixins — the ones that state obligations — and the marker names the contract side of a mixin, not a different construct. A mixin that requires nothing of its host declares no contract member and is no protocol: it carries no `P` marker and is classified by the ordinary clauses (`C_`/`S_`).
- **Guidance**: prefer decomposing a hybrid design — a protocol that also implements a dynamic contract (`PAC_`, or a `PC_` mixin over an interface) — into a dynamic base (`IC_`/`AC_`) plus a standalone `PC_` mixin.
- **Variable markers never encode role markers**: the abstraction level and protocol nature of a type are carried by the type name alone (`renderable`\_`p` regardless of whether it points to an `IC_`, `AC_` or `C_` type). Pairing a protocol with a same-named concept (`PC_Drawable` ↔ `concept Drawable`) is a common arrangement, but concept naming lies outside this document: the pair above is an illustration, not a rule.

***Example 1***:

```C++
struct IS_Drawable                            // interface struct
{
    virtual ~IS_Drawable() = default;
    virtual void draw() const = 0;
};

struct IS_Serializable                        // interface struct: a second, independent contract
{
    virtual ~IS_Serializable() = default;
    virtual void serialize() const = 0;
};

struct IS_Savable : IS_Drawable, IS_Serializable   // composite interface: declares nothing of its own
{
};

class C_Icon final : public IS_Savable        // implements both aggregated contracts
{
public:
    void draw() const override;
    void serialize() const override;
};

class AC_WidgetBase : public IS_Drawable      // abstract class: adds a field
{
public:
    void draw() const override = 0;

protected:
    int prot_width;
};

class C_Button final : public AC_WidgetBase   // concrete implementation
{
public:
    void draw() const override;
};
```

***Example 2***:

```C++
// IS_Drawable: the interface of Example 1 above, declared again here so that this
// fragment compiles on its own
struct IS_Drawable
{
    virtual ~IS_Drawable() = default;
    virtual void draw() const = 0;
};

template <typename TTP_Derived>
class PC_Refreshable                          // protocol class (CRTP mixin)
{
public:
    void refresh() { static_cast<TTP_Derived&>(*this).refreshState(); }

protected:
    // destruction rule: protected non-virtual, so deletion through a protocol
    // pointer cannot be written
    ~PC_Refreshable() = default;
};

class C_Ticker final : public PC_Refreshable<C_Ticker>
{
public:
    void refreshState();
};

template <typename TTP_Derived>
class PAC_PanelBase : public IS_Drawable      // abstract protocol: pure virtual + forwarding + field
{
public:
    void draw() const override = 0;
    void refresh() { static_cast<TTP_Derived&>(*this).refreshState(); }

protected:
    int prot_width;
};

class C_MainPanel final : public PAC_PanelBase<C_MainPanel>
{
public:
    void draw() const override;
    void refreshState();
};
```

#### `1.2.3. Type alias prefixes (prefixes for types created via using/typedef keywords)`

- `TA`: `type` `alias` to some primitive type (`TA` - `T`ype `A`lias)
- `TAC`: `type` `alias` to some `class` type (`TAC` - `T`ype `A`lias `C`lass)
- `TAS`: `type` `alias` to some `struct` type (`TAS` - `T`ype `A`lias `S`truct)
- `TAE`: `type` `alias` to some `enum` type (`TAE` - `T`ype `A`lias `E`num)
- `TAU`: `type` `alias` to some `union` type (`TAU` - `T`ype `A`lias `U`nion)
- `TAP`: `type` `alias` to some `pointer` type (`TAP` - `T`ype `A`lias `P`ointer)
- `TAR`: `type` `alias` to some `reference` type (`TAR` - `T`ype `A`lias `R`eference)
- `TAF`: `type` `alias` to some `function` type (`TAF` - `T`ype `A`lias `F`unction)
- `TAA`: `type` `alias` to some `array` type (`TAA` - `T`ype `A`lias `A`rray)
- `TAM`: `type` `alias` to some `pointer` `to` `member` type (`TAM` - `T`ype `A`lias `M`ember)
- `TAIC`: `type` `alias` to some `interface class` type (`TAIC` - `T`ype `A`lias `I`nterface `C`lass)
- `TAAC`: `type` `alias` to some `abstract class` type (`TAAC` - `T`ype `A`lias `A`bstract `C`lass)
- `TAIS`: `type` `alias` to some `interface struct` type (`TAIS` - `T`ype `A`lias `I`nterface `S`truct)
- `TAAS`: `type` `alias` to some `abstract struct` type (`TAAS` - `T`ype `A`lias `A`bstract `S`truct)
- `TAPC`: `type` `alias` to some `protocol class` type (`TAPC` - `T`ype `A`lias `P`rotocol `C`lass)
- `TAPS`: `type` `alias` to some `protocol struct` type (`TAPS` - `T`ype `A`lias `P`rotocol `S`truct)
- `TAPAC`: `type` `alias` to some `abstract protocol class` type (`TAPAC` - `T`ype `A`lias `P`rotocol `A`bstract `C`lass)
- `TAPAS`: `type` `alias` to some `abstract protocol struct` type (`TAPAS` - `T`ype `A`lias `P`rotocol `A`bstract `S`truct)

**Important notice for aliases of aliases**:

> A `using`/`typedef` declaration introduces no new type — an alias is just another name for the underlying type. Therefore, an alias of another alias must be named according to the *resolved* underlying type's category (e.g., aliasing a `TAC_SomeType` still yields a `TAC_…` name): an alias of an alias has no prefix of its own. The resolved underlying category includes role markers (e.g., aliasing a `PAC_SomeType` yields a `TAPAC_…` name, preserving the `[P][A][kind]` marker order).

**Important notice for array and member-pointer aliases**:

> `TAA` and `TAM` name the outermost kind only, exactly like `TAP`, `TAR` and `TAF`, and take no `type letter`: `using TAA_FrameBuffer = char[4];` and `using TAM_RenderHandler = void (C_Renderer::*)();` say nothing about the element type or about the class that owns the member. A pointer to an array is a `pointer` and keeps `TAP` (`using TAP_FrameBuffer = char (*)[4];`); a pointer to a member is `TAM` whether it designates a member object or a member function. `TAA` never carries `role markers`: `TAAC_` and `TAAS_` are read as `TA` + `AC`/`AS` (an abstract class, an abstract struct), never as `TAA_` + `C`/`S`. An alias never changes what the variable is: a variable of `TAP_IntPtr` is a pointer variable (`ptr_gp`), and one of an aliased array or member-pointer type takes no kind marker — a type prefix exists because such a type has no other way to be named, and it does not make the variable a kind (see the notice in [Reference markers](#116-reference-markers)).

***Example 1***:

```C++
enum class E_SomeType { Enum1, Enum2 };

using TAE_SomeType = E_SomeType;

E_SomeType var_ge = E_SomeType::Enum1;

const TAE_SomeType someVar_gce = var_ge;
```

- `TAE_SomeType`: A `type alias` for `enum class` type (`E_SomeType`)
- `var`\_`ge`: A `global enum` variable (instance) of `enum class` type (`E_SomeType`), marked with the `enum` marker (`e`)
- `someVar`\_`gce`: A `global const enum` variable (instance) of `enum class` type (`E_SomeType`), marked with the `enum` marker (`e`)

***Example 2***:

```C++
class C_SomeType {};

using TAC_SomeType = C_SomeType;

C_SomeType var_g;

const TAC_SomeType* someVar_gpc = &var_g;
```

- `TAC_SomeType`: A `type alias` for `class` type (`C_SomeType`)
- `var`\_`g`: A `global` variable (instance) of `class` type (`C_SomeType`)
- `someVar`\_`gpc`: A `global pointer to const` object of `class` type (`C_SomeType`), marked with the `pointer-to-const` variant of the `pointer` marker (`pc`)

***Example 3***:

```C++
struct S_SomeType {};

using TAS_SomeType = S_SomeType;

S_SomeType var_g;

const TAS_SomeType& someVar_grc = var_g;
```

- `TAS_SomeType`: A `type alias` for `struct` type (`S_SomeType`)
- `var`\_`g`: A `global` variable (instance) of `struct` type (`S_SomeType`)
- `someVar`\_`grc`: A `global reference to const` object of `struct` type (`S_SomeType`), marked with the `reference-to-const` variant of the `reference` marker (`rc`)

### `1.3. Template parameters`

#### `1.3.1. Type template parameter prefixes`

- `TTP`: `type` `template` `parameter` (`TTP` - `T`ype `T`emplate `P`arameter)
- `TTPP`: `type` `template` `parameter` `pack` (`TTPP` - `T`ype `T`emplate `P`arameter `P`ack)

#### `1.3.2. Non-type template parameter prefixes`

- `NTTP`: `non` `type` `template` `parameter` (`NTTP` - `N`on `T`ype `T`emplate `P`arameter)
- `NTTPP`: `non` `type` `template` `parameter` `pack` (`NTTPP` - `N`on `T`ype `T`emplate `P`arameter `P`ack)

#### `1.3.3. Template template parameter prefixes`

- `TeTP`: `template` `template` `parameter` (`TeTP` - `Te`mplate `T`emplate `P`arameter)
- `TeTPP`: `template` `template` `parameter` `pack` (`TeTPP` - `Te`mplate `T`emplate `P`arameter `P`ack)

## `2. File naming conventions`

| Entity                          | Convention                          | Example              |
|:------------------------------- | ----------------------------------- | -------------------- |
| Implementation/Source file name | noun in `snake_case.cpp` style-form | `frame_renderer.cpp` |
| Header file name                | noun in `snake_case.hpp` style-form | `frame_renderer.hpp` |

**Important notice for the file name and the entity it holds**:

> The noun names what the file exists to declare: a file that declares one primary type names it with the type prefix dropped (`C_FrameRenderer` lives in `frame_renderer.cpp` and `frame_renderer.hpp`); a file that declares no single primary type — a utility translation unit, a set of free functions — takes the name of what the file as a whole provides. A few illustrative fragments in this document name no entity at all (the ultimate example is a rules exercise, not a component), and their hypothetical artifact names follow the same style-form without corresponding to any type.

## `3. Namespace naming conventions`

| Entity          | Convention              | Example                                         |
|:--------------- | ----------------------- | ----------------------------------------------- |
| Namespaces      | `snake_case` style-form | `frame_renderer`                                |
| Namespace alias | `snake_case` style-form | `render` (`namespace render = frame_renderer;`) |

## `4. Type naming conventions`

| Entity          | Convention                           | Example             |
|:--------------- | ------------------------------------ | ------------------- |
| Type name       | noun in `type-name` style-form       | `C_FrameRenderer`   |
| Type alias name | noun in `type-alias-name` style-form | `TAC_FrameRenderer` |

## `5. Function-like Macro and Function/Method naming conventions`

| Entity                   | Convention                                       | Example                          |
|:------------------------ | ------------------------------------------------ | -------------------------------- |
| Function-like macro name | imperative verb in `UPPER_SNAKE_CASE` style-form | `SAVE_DATA(destination, source)` |
| Function/Method name     | imperative verb in `camelCase` style-form        | `sendRequest(value)`             |

**Important notice for member-method calls**:

> Non-`static` member methods **must** be called from within the class's own methods exclusively via the `this->` qualifier (e.g., `this->resizeBuffer()`), so that it is always obvious a call targets an instance method rather than a free function. `static` member methods, conversely, **must** be qualified with the enclosing class name (e.g., `C_SomeType::create()`) and **must never** be called via `this->`. Member *fields* are the exact opposite: they are never accessed through `this->`, because the access marker already identifies them (see [Member variable naming conventions](#8-member-variable-naming-conventions)). A call that does not go through `this` is not a `this->` call and keeps the form of its own expression — a CRTP hook reached as `static_cast<TTP_Derived&>(*this).refreshState()` (see [Abstraction & protocol markers](#122-abstraction--protocol-markers)), a call on another object, and a call on a base subobject.

**Important notice for function and method names**:

> The imperative-verb form applies to every function and method this document names, hooks included: a protocol's hook is an action of the host type like any other method, so the forwarder stays `refresh()` and the hook it calls is `refreshState()` — a hook name such as `onRefresh` is not valid. The only function names the rule cannot cover are the ones fixed for us: names the language itself defines (`main`, constructors, destructors, conversion operators, `operator+`) and names an existing system or third-party interface keeps in place (an override of a library virtual such as `std::exception::what()`). These are the function-side cases of the deviations listed in [Scope and permitted deviations](#scope-and-permitted-deviations). A method that answers a question rather than performs an action keeps the verb-first predicate form (`isVisible()`, `hasError()`), with the same predicate verbs a `bool` variable takes (see the Boolean notice in [Variable markers](#11-variable-markers)).

**Important notice for a function's own linkage**:

> A function name carries no marker: the markers of §1.1 describe variables, and no call site reads a function's linkage. A function the project exposes to its users keeps its plain `camelCase` name; a helper only its own translation unit uses is declared in an anonymous (unnamed) namespace and keeps exactly the same form (`int scaleFactorFor(int value)`), because it is the namespace that makes the linkage internal in the language itself. The `static` keyword is not written for such a helper — it would only repeat what the namespace already guarantees, exactly as it does for a variable (see [Scope markers](#111-scope-markers)) — and no marker ever appears on a function name: neither the [`scope`] `a` nor a [`storage-class`] `s` or `x`.

**Important notice for the parentheses in the examples**:

> Parentheses are never part of a name: they appear in the tables and examples to show how the entity is written where it is used — a function-like macro with its argument list (`SAVE_DATA(destination, source)`), a function or method with its parameter list (`sendRequest(value)`). The names themselves are `SAVE_DATA` and `sendRequest`. The parameters of a function-like macro are block-scope names like any other, so no [`scope`] marker applies to them; and because no storage class, cv-qualifier or kind can be attached to a macro parameter, they are written as bare nouns.

## `6. Object-like Macro and Enumerator naming conventions`

| Entity                              | Convention                                | Example           |
|:----------------------------------- | ----------------------------------------- | ----------------- |
| Object-like macro name              | noun in `UPPER_SNAKE_CASE` style-form     | `MAX_BUFFER_SIZE` |
| Enumerator name for enum-class type | any name in `PascalCase` style-form       | `DeepPurple`      |
| Enumerator name for enum type       | any name in `UPPER_SNAKE_CASE` style-form | `DEEP_PURPLE`     |

**Rationale for enumerator naming**:

> For backward compatibility with C-style conventions, plain `enum` enumerators use `UPPER_SNAKE_CASE` (e.g., `DEEP_PURPLE`). For `enum class` enumerators, the mandatory type-name qualifier `E_EnumType::` allows the enumerator name itself to be written in `PascalCase` instead of `UPPER_SNAKE_CASE`, yielding the full form `E_Color::DeepPurple`. Neither enumerator row asks for a noun: unlike a variable or an object-like macro, an enumerator names a value rather than an object, so its casing is the only requirement.

**Important notice for constants without a marker**:

> An object-like macro and an enumerator are the only constant-like names in this document that carry no marker: neither is a variable, so the `c` [`cv-qualifier`] marker never applies to them (see the notice in [CV-qualifier markers](#113-cv-qualifier-markers)). The boundary is the declaration, not the value: `#define MAX_BUFFER_SIZE 256` is a macro and stays `MAX_BUFFER_SIZE`, while a variable holding the same value — `constexpr int maxBufferSize`\_`gc = 256;` — is a variable and takes the marker. A `const`-like variable is therefore never written in `UPPER_SNAKE_CASE`, and a macro is never given a marker block.

## `7. Non-Member variable naming conventions`

The forms below are minimal: the examples are block-scope names, so a non-member variable declared in a namespace adds its [`scope`] marker (`operatingMode`\_`ge`) and one declared in a class adds its access marker instead (see [Member variable naming conventions](#8-member-variable-naming-conventions)).

| Entity                   | Convention                           | Example              |
|:------------------------ |:------------------------------------ |:-------------------- |
| Enum variable name       | noun in `enum-var` style-form        | `operatingMode`\_`e` |
| Pointer variable name    | noun in `pointer-var` style-form     | `dataBuffer`\_`p`    |
| Reference variable name  | noun in `reference-var` style-form   | `dataBuffer`\_`r`    |
| Ordinary variable name   | noun in `normal-var` style-form      | `operatingMode`      |
| Boolean variable name    | predicate in `normal-var` style-form | `isVisible`          |

## `8. Member variable naming conventions`

The **base name** of a member variable is the same meaningful noun in `camelCase` — or the predicate of a `bool` (see [Variable markers](#11-variable-markers)) — as for a non-member variable, and it carries the same marker block after it; a member *function* carries no access marker and is named by [Function-like Macro and Function/Method naming conventions](#5-function-like-macro-and-functionmethod-naming-conventions). On top of that, the requirements below apply.

| Entity                    | Convention                                                                                                                              | Example                                             |
|:------------------------- |:--------------------------------------------------------------------------------------------------------------------------------------- |:--------------------------------------------------- |
| Instance member variable  | noun in `camelCase` (or the predicate of a `bool`) with the access marker and the marker block of its style-form, no [`scope`] position | `pub`\_`operatingMode`, `prot`\_`targetState`\_`e`  |
| `static` member variable  | the same, with the `s` (or `st`) [`storage-class`] marker                                                                               | `pub`\_`instanceCount`\_`s`                         |

**Important notice for the access marker and member scope**:

> Every **member variable** — `static` or not — carries a mandatory **access marker** as its leading prefix — `pub_`, `prot_` or `priv_` — and omits the [`scope`] marker entirely: a member is *class-scoped*, never namespace-scoped, so `g` / `n` / `a` never apply to a member variable. A member *function* carries no access marker: functions are named by the [Function-like Macro and Function/Method naming conventions](#5-function-like-macro-and-functionmethod-naming-conventions), never by this section. What follows the base name is the same trailing marker block as for any other variable: [`access-marker`]\_`camelCase`\_, then the block of the variable's own style-form with the [`scope`] position dropped — [`storage-class`][`cv-qualifier`] and at most one kind marker ([`enum`], [`pointer`] or [`reference`]; a reference carries no [`cv-qualifier`] marker at all) — and, exactly as for a non-member variable, a member whose block has nothing to mark is written without the trailing underscore (`pub`\_`operatingMode`):
>
> - An ordinary (instance) non-static member carries **no storage-class marker** (e.g., `pub`\_`operatingMode`, `prot`\_`operatingMode`\_`pe`).
> - A `static` class member carries the **`s`** storage-class marker (e.g., `pub`\_`instanceCount`\_`s`) — the *class-level shared storage* reading of the same marker [Storage-class markers](#112-storage-class-markers) defines at namespace scope: the kind of scope the variable sits in decides which reading applies. The `x` (`extern`) marker is **never** used on members: `static` members are defined exactly once and resolved by the linker; a declaration of one is written in the header with the plain `s` marker and defined in one source file with the same `s` marker (the keyword `static` is omitted at the definition).
> - `static thread_local` members carry **`st`** (e.g., `pub`\_`cache`\_`st`), mirroring the namespace-scope storage-class markers. A bare `t` never appears on a member: a non-`static` data member cannot be declared `thread_local` at all, so `static thread_local` is the only `thread_local` form a member can take.
>
> The access marker is always the leading prefix and the marker block is always trailing; the two never merge, swap places, or absorb one another (see [Members combining the access marker and the marker block](#82-members-combining-the-access-marker-and-the-marker-block)).

Access rules:

- Non-`static` fields declared in a class are accessed **bare** — without the `this->` qualifier, but always with the marker the name carries (e.g., `prot`\_`operatingMode`\_`pe`, never `this->prot_operatingMode_pe`). The `this->` qualifier is **forbidden** on fields: the access marker already makes it obvious that the name denotes a class field, so the qualifier adds nothing but noise.
- `static` members are **not** accessed via `this->` (they have no instance). They **must** be qualified with their enclosing class name (e.g., `C_SomeType`::`pub`\_`instanceCount`\_`s`) even from within the class's own methods, so that the access is unambiguously a class-level entity.
- Access from outside the class uses the object or the pointer — `obj`.`pub`\_`operatingMode` and `ptr`->`pub`\_`operatingMode` — once again with the member's full name.

A member's name is identical wherever it is written, inside or outside the class; only the qualifier that selects the object differs:

| Access level | Leading marker | Inside class methods          | Outside the class (via object/pointer)                                                            |
|:------------ |:-------------- |:----------------------------- | ------------------------------------------------------------------------------------------------- |
| `public`     | `pub_`         | `pub`\_`accessCount`          | `obj`.`pub`\_`accessCount` / `ptr`->`pub`\_`accessCount`                                          |
| `protected`  | `prot_`        | `prot`\_`operatingMode`\_`pe` | `obj`.`prot`\_`operatingMode`\_`pe` / `ptr`->`prot`\_`operatingMode`\_`pe` (derived classes only) |
| `private`    | `priv_`        | `priv`\_`targetState`\_`e`    | Not accessible (except to `friend`s and nested classes)                                           |

### `8.1. Mutable members`

The `mutable` keyword is orthogonal to access level and to all marker categories: it governs whether a field may be modified through a `const`-qualified method, not the field's scope, storage, or type. `mutable` members therefore follow exactly the same naming rules as non-`mutable` members of the same access level; the `mutable` qualifier is intentionally not encoded in the name.

***Example***:

```C++
#include <cstddef>

enum E_CacheState { CACHE_EMPTY, CACHE_FILLED };

class C_Cache {
public:
    mutable std::size_t pub_accessCount;      // mutable public:    access marker only
protected:
    mutable E_CacheState prot_state_e;        // mutable protected: access marker + marker block
private:
    mutable E_CacheState priv_replacement_e;  // mutable private:   same rules as any other member
};

// inside a const method:
// pub_accessCount++;
// prot_state_e;
// priv_replacement_e;
```

### `8.2. Members combining the access marker and the marker block`

***Example***:

```C++
enum E_OperatingMode { MODE_READ, MODE_WRITE };

class C_SomeType {
protected:
    E_OperatingMode* prot_operatingMode_pe;  // protected pointer member
private:
    E_OperatingMode priv_targetState_e;     // private enum-typed member
};

// access:
// prot_operatingMode_pe;
// priv_targetState_e;
```

## `9. Template parameter naming conventions`

| Entity                            | Convention                            | Example          |
|:--------------------------------- | ------------------------------------- | ---------------- |
| Type template parameter           | noun in `TTP_PascalCase` style-form   | `TTP_Value`      |
| Protocol's derived-type parameter | fixed name `TTP_Derived`              | `TTP_Derived`    |
| Type template parameter pack      | noun in `TTPP_PascalCase` style-form  | `TTPP_Args`      |
| Non-type template parameter       | noun in `NTTP_PascalCase` style-form  | `NTTP_Count`     |
| Non-type template parameter pack  | noun in `NTTPP_PascalCase` style-form | `NTTPP_Values`   |
| Template template parameter       | noun in `TeTP_PascalCase` style-form  | `TeTP_Allocator` |
| Template template parameter pack  | noun in `TeTPP_PascalCase` style-form | `TeTPP_Policies` |

**Important notice for the derived-type parameter**:

> A protocol's derived-type template parameter is always named `TTP_Derived`: the clause that recognizes a contract member (clause `P1`) reads that name, so it is part of the protocol form rather than a free noun — see [Abstraction & protocol markers](#122-abstraction--protocol-markers).

## `10. Ultimate compilable example`

A single, self-contained translation unit (example) that exercises the naming conventions defined in this document; the coverage list at its end names the few it points at instead of demonstrating. This example is artificial by design. The file-name convention is represented by the hypothetical artifact name `ultimate_example.cpp`, and the namespace-name convention is demonstrated by the `snake_case` namespaces below.

```C++
// ============================================================================
// Ultimate compilable example
// File-name convention: ultimate_example.cpp  Namespace convention: snake_case
// ============================================================================

// ---- Macros (object-like + function-like) ----
#define MAX_BUFFER_SIZE 256                                           // object-like macro: UPPER_SNAKE_CASE
#define SAVE_DATA(destination, source) ((void)((destination) = (source)))  // function-like macro: UPPER_SNAKE_CASE

// ---- Types ----
enum       E_DeviceState { STATE_IDLE, STATE_RUNNING, STATE_ERROR };  // plain enum; enumerators UPPER_SNAKE_CASE
enum class E_Color       { DeepPurple, LightBlue };                   // enum class; enumerators PascalCase
struct     S_Point       { int pub_x; int pub_y; };                   // struct type
union      U_Packet      { int pub_raw; float pub_floating; };        // union type
class      C_Renderer {};                                             // class type
struct     IS_Drawable;                                               // interface struct type (forward)

// ---- Type aliases (using) ----
using TA_Count     = unsigned;       // alias to primitive
using TAC_Renderer = C_Renderer;     // alias to class
using TAS_Point    = S_Point;        // alias to struct
using TAE_Color    = E_Color;        // alias to enum
using TAU_Packet   = U_Packet;       // alias to union
using TAP_IntPtr   = int*;           // alias to pointer
using TAR_IntRef   = int&;           // alias to reference
using TAF_BinaryOp = int(int, int);  // alias to function
using TAA_FrameBuffer   = char[4];                 // alias to array
using TAP_FrameBuffer   = char (*)[4];              // alias to pointer to array (a pointer keeps TAP)
using TAM_Offset        = int S_Point::*;          // alias to pointer to object member
using TAM_RenderHandler = void (C_Renderer::*)();  // alias to pointer to function member

using TAIS_Drawable = IS_Drawable;   // alias to interface struct (marker-aware)

// ============================================================================
// Global-namespace variables
// ============================================================================
int                     someVar_g   = 20;                    // scope = g
static int              someVar_gs  = 21;                    // g + static(internal linkage)
thread_local int        someVar_gt  = 22;                    // g + thread_local
static thread_local int someVar_gst = 23;                    // g + static thread_local
const int               someVar_gc  = 24;                    // g + const
volatile int            someVar_gv  = 25;                    // g + volatile
const volatile int      someVar_gcv = 0;                     // g + const volatile
constexpr int           someConstVar_gc  = 26;               // g + constexpr (const-like -> `c`)
static constexpr int    someConstVar_gsc = 27;               // g + static + constexpr (const-like -> `c`)

extern int              someVar_gx;                          // extern declaration (defined elsewhere)
extern thread_local int someVar_gxt;                         // extern thread_local declaration

// global enum variables
E_DeviceState                someState_ge     = STATE_IDLE;  // scope = g + enum
const E_DeviceState          someState_gce    = STATE_IDLE;  // g + const + enum
const volatile E_DeviceState targetState_gcve = STATE_IDLE;  // g + const volatile + enum
constexpr E_Color            someColor_gce     = E_Color::DeepPurple;  // g + constexpr + enum (const-like)

// targets for pointers / references
int                          intTarget_g     = 30;
const int                    intTarget_gc    = 31;
volatile int                 intTarget_gv    = 32;
const volatile int           intTarget_gcv   = 0;

// states for pointers / references
E_DeviceState                state_ge   = STATE_RUNNING;
const E_DeviceState          state_gce  = STATE_RUNNING;
volatile E_DeviceState       state_gve  = STATE_RUNNING;
const volatile E_DeviceState state_gcve = STATE_RUNNING;

// pointer variables
int*                                                intTarget_gp   = &intTarget_g;    // pointer
const int*                                          intTarget_gpc  = &intTarget_gc;   // pointer to const
volatile int*                                       intTarget_gpv  = &intTarget_gv;   // pointer to volatile
const volatile int*                                 intTarget_gpcv = &intTarget_gcv;  // pointer to const volatile
E_DeviceState*                                      state_gpe      = &state_ge;       // pointer to enum
const E_DeviceState*                                state_gpce     = &state_gce;      // pointer to const enum
volatile E_DeviceState*                             state_gpve     = &state_gve;      // pointer to volatile enum
const volatile E_DeviceState*                       state_gpcve    = &state_gcve;     // pointer to const volatile enum
static const volatile E_DeviceState* const volatile state_gscvpcve = &state_gcve;     // static cv pointer to cv enum

// reference variables — no cv-qualifier marker for references
int&                                 intTarget_gr   = intTarget_g;    // reference
const int&                           intTarget_grc  = intTarget_gc;   // reference to const
volatile int&                        intTarget_grv  = intTarget_gv;   // reference to volatile
const volatile int&                  intTarget_grcv = intTarget_gcv;  // reference to const volatile
E_DeviceState&                       state_gre      = state_ge;       // reference to enum
const E_DeviceState&                 state_grce     = state_gce;      // reference to const enum
volatile E_DeviceState&              state_grve     = state_gve;      // reference to volatile enum
const volatile E_DeviceState&        state_grcve    = state_gcve;     // reference to const volatile enum
static const volatile E_DeviceState& state_gsrcve   = state_gcve;     // static reference to a cv enum

// array and member-pointer variables: no kind marker — an array is not a pointer,
// and a member pointer designates a member rather than an object
TAA_FrameBuffer   frameBuffer_g   = {'a', 'b', 'c', 'd'};
TAP_FrameBuffer   frameBuffer_gp  = &frameBuffer_g;
TAM_Offset        offset_g        = &S_Point::pub_x;
TAM_RenderHandler renderHandler_g = nullptr;

// ============================================================================
// Named namespace (snake_case): frame_renderer
// ============================================================================
namespace frame_renderer
{
    int                     someVar_n     = 1;           // scope = n
    static int              someVar_ns    = 2;           // n + static
    thread_local int        someVar_nt    = 3;           // n + thread_local
    static thread_local int someVar_nst   = 4;           // n + static thread_local
    const int               someVar_nc    = 5;           // n + const
    const volatile int      someVar_ncv   = 0;           // n + const volatile
    E_DeviceState           someState_ne  = STATE_IDLE;  // n + enum
    const E_DeviceState     someState_nce = STATE_IDLE;  // n + const + enum

    int*                    ptr_np = nullptr;            // n + pointer
    E_DeviceState*          ptr_npe = &someState_ne;     // n + pointer to enum
    E_DeviceState&          ref_nre = someState_ne;      // n + reference to enum

    extern thread_local int someVar_nxt;                 // n + extern declaration; the definition is elsewhere

    int computeFrameSum(int leftValue, int rightValue) { return leftValue + rightValue; }  // function: camelCase
}

namespace render = frame_renderer;  // namespace alias: snake_case

// ============================================================================
// Anonymous namespace (marker `a`; mutually exclusive with `static`)
// ============================================================================
namespace
{
    int                  someVar_a      = 10;            // scope = a
    const int            someVar_ac     = 11;            // a + const
    E_DeviceState        someState_ae   = STATE_IDLE;    // a + enum
    int*                 someVar_ap     = &someVar_a;    // a + pointer
    const E_DeviceState& someState_arce = someState_ae;  // a + reference to const enum
    thread_local int     someVar_at     = 12;            // a + thread_local (duration, not linkage)
    // a static (`as`, `ast`) or extern (`ax`, `axt`) here is forbidden: the `a` marker excludes `s` and `x`
    // a helper function with internal linkage: the same form, no marker
    int scaleFactorFor(int value) { return value * 2; }
}

// ============================================================================
// Free function (camelCase) demonstrating local-scope variables
// (block scope: no scope marker; the marker block starts at the storage-class position)
// ============================================================================
void demonstrateLocals()
{
    int                 someVar      = 0;            // local (no markers)
    static int          someVar_s    = 0;            // local + static
    thread_local int    someVar_t    = 0;            // local + thread_local
    const int           someVar_c    = 1;            // local + const
    constexpr int       someConstVar_c = 7;          // local + constexpr (const-like)
    E_DeviceState       someState_e  = STATE_IDLE;   // local + enum
    const E_DeviceState someState_ce = STATE_IDLE;   // local + const enum
    int*                dataBuffer_p = nullptr;      // local + pointer
    const int&          someVar_rc   = someVar;      // local + reference to const
    E_DeviceState&      someState_re = someState_e;  // local + reference to enum
    bool                isVisible    = true;         // local + predicate (bool)
    auto [xCoordinate, yCoordinate] = S_Point{1, 2}; // structured binding: block scope, no marker block
    (void) xCoordinate;
    (void) yCoordinate;
}

int sendRequest(int value) { return value; }  // free function: camelCase

// ============================================================================
// Class members: access markers (public: `pub_`, protected: `prot_`, private: `priv_`)
// Fields bare (no this->); non-static methods via this->; static members/methods via C_Logger::...
// ============================================================================
class C_Logger
{
public:
    int         pub_someField;        // public: access marker only
    mutable int pub_accessCount;      // public, mutable: access marker only (mutable not encoded)
    int*        pub_outputBuffer_p;   // public pointer member: access marker + pointer marker
    static int  pub_instanceCount_s;  // public static member (declaration)

protected:
    int            prot_protectedField;    // protected: access marker only
    E_DeviceState  prot_logState_e;        // protected enum member
    E_DeviceState* prot_operatingMode_pe;  // protected pointer-to-enum member

private:
    int           priv_privateField;   // private: access marker only
    E_DeviceState priv_targetState_e;  // private enum member
    const int     priv_limit_c;        // private const member: access marker + cv-qualifier marker
    static int    priv_someCounter_s;  // private static member (declaration)

public:
    static inline thread_local int pub_cache_st = 0;  // static thread_local member
    static constexpr int pub_maxBufferSize_sc = MAX_BUFFER_SIZE;  // static constexpr member (const-like)

    C_Logger()
        : pub_someField(0), pub_accessCount(0), pub_outputBuffer_p(nullptr),
          prot_protectedField(0), prot_logState_e(STATE_IDLE), prot_operatingMode_pe(nullptr),
          priv_privateField(0), priv_targetState_e(STATE_IDLE), priv_limit_c(MAX_BUFFER_SIZE)
    {}

    void flushBuffer()  // non-static helper method (camelCase)
    {
        pub_someField = 0;
    }

    void logMessage()
    {
        pub_someField++;
        pub_accessCount++;
        prot_protectedField++;
        prot_logState_e = STATE_RUNNING;
        prot_operatingMode_pe = &prot_logState_e;
        priv_privateField++;
        priv_targetState_e = STATE_ERROR;
        this->flushBuffer();          // non-static method call: this->method()
        C_Logger::pub_instanceCount_s++;
        C_Logger::priv_someCounter_s++;
        C_Logger::resetCount();       // static method call: C_Logger::method()
    }

    void touch() const { pub_accessCount++; }  // mutable modified through const method

    static int resetCount()
    {
        C_Logger::priv_someCounter_s = 0;
        return C_Logger::pub_instanceCount_s;
    }
};

// static member definitions: keyword `static` omitted; the same name, storage marker included
int C_Logger::pub_instanceCount_s = 0;
int C_Logger::priv_someCounter_s = 0;

// ============================================================================
// Role-marked types: interface / abstract / protocol / abstract protocol
// ============================================================================
struct IS_Drawable
{
    virtual ~IS_Drawable() = default;
    virtual void draw() const = 0;
};

class AC_WidgetBase : public IS_Drawable  // abstract class: virtual + field
{
public:
    void draw() const override = 0;

protected:
    int prot_width;
};

class C_Button final : public AC_WidgetBase  // concrete implementation
{
public:
    void draw() const override {}
};

template <typename TTP_Derived>
class PC_Refreshable  // protocol class (static contract, no virtual functions)
{
public:
    void refresh() { static_cast<TTP_Derived&>(*this).refreshState(); }

protected:
    // destruction rule: protected non-virtual, so deletion through a
    // protocol pointer cannot be written
    ~PC_Refreshable() = default;
};

class C_Ticker final : public PC_Refreshable<C_Ticker>
{
public:
    void refreshState() {}
};

template <typename TTP_Derived>
class PAC_PanelBase : public IS_Drawable  // abstract protocol: pure virtual + forwarding + field
{
public:
    void draw() const override = 0;
    void refresh() { static_cast<TTP_Derived&>(*this).refreshState(); }

protected:
    int prot_width;
};

class C_MainPanel final : public PAC_PanelBase<C_MainPanel>
{
public:
    void draw() const override {}
    void refreshState() { ++prot_width; }
};

template <typename TTP_Derived>
class PC_DrawMixin : public IS_Drawable  // mixin over an interface: static + dynamic contract
{
public:
    void draw() const override { static_cast<const TTP_Derived&>(*this).drawContent(); }
    void refresh() { static_cast<TTP_Derived&>(*this).refreshState(); }
};

class C_Tile final : public PC_DrawMixin<C_Tile>
{
public:
    void drawContent() const {}
    void refreshState() {}
};

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
    C_Container() : prot_value(), prot_state_e(STATE_IDLE), priv_internal(0), priv_isDirty(false) {}

    TTP_Value retrieve() const { return prot_value; }

    void update()
    {
        prot_value = TTP_Value{};
        prot_state_e = STATE_RUNNING;
        priv_internal++;
        C_Container::pub_sharedCount_s++;
        C_Container::priv_privateTotal_s++;
    }

    static inline int pub_sharedCount_s = 0;  // public static inline member

protected:
    TTP_Value     prot_value;    // protected: access marker only
    E_DeviceState prot_state_e;  // protected enum member

private:
    int               priv_internal;            // private: access marker only
    bool              priv_isDirty;             // private Boolean: predicate base name
    static inline int priv_privateTotal_s = 0;  // private static inline member
};

// ============================================================================
// Entry point exercising the runnable surface
// ============================================================================
int main()
{
    C_Logger logger;
    logger.logMessage();                // external call on an object; inside the class, methods are called via this->
    logger.touch();
    logger.pub_outputBuffer_p = nullptr;    // public field access from outside (obj.member)
    int instanceCount = C_Logger::pub_instanceCount_s;  // static member access qualified by class name
    C_Logger::resetCount();

    C_Logger* logger_p = &logger;       // local pointer variable (block scope: no scope marker)
    logger_p->pub_someField = 0;            // public field access via pointer (ptr->member)

    sendRequest(0);
    frame_renderer::computeFrameSum(1, 2);
    render::computeFrameSum(3, 4);      // the same function through the namespace alias
    demonstrateLocals();

    C_Ticker ticker;
    ticker.refresh();                   // static dispatch through protocol base (no vtable)

    C_MainPanel panel;
    panel.refresh();                    // abstract protocol forwarding
    IS_Drawable& drawable_r = panel;    // local reference to interface (block scope: no scope marker)
    drawable_r.draw();                  // virtual dispatch through the interface

    C_Tile tile;
    tile.refresh();                     // mixin over an interface: static obligation served through the protocol
    tile.draw();                        // mixin over an interface: implemented dynamic contract

    (void) instanceCount;

    frameBuffer_g[0] = 'z';             // array variable (no kind marker): element access
    (*frameBuffer_gp)[1] = 'y';         // pointer to an array: still a pointer variable
    offset_g = nullptr;                 // member-pointer variable (no kind marker)
    renderHandler_g = nullptr;          // member-pointer variable to a member function

    return 0;
}
```

This example covers:

- **File and namespace conventions** — the artifact name `ultimate_example.cpp`, the `snake_case` namespace `frame_renderer`, and the `snake_case` alias `render`.
- **Scope and storage markers** — `g`, `n`, `a` and their omission at local and member scope, the `a` + `thread_local` combination (`at`) and the forbidden `as` / `ast` / `ax` / `axt`; `s`, `t` and `st` at namespace scope (`gs`, `gt`, `gst`, `ns`, `nt`, `nst`) with `s` and `st` as class members (a bare `t` has no member form — see [Member variable naming conventions](#8-member-variable-naming-conventions)); and the out-of-line static-member definition pattern (keyword `static` omitted, the name retained unchanged).
- **Extern declarations** — the `gx`, `gxt` and `nxt` markers, marked as declarations whose definition is elsewhere.
- **cv-qualifier markers** — all three (`c`, `v`, `cv`) at namespace scope, and the `c` case at local and member scope, including the `const`-like form: a `constexpr` variable takes the same `c` marker as a `const` one (`someConstVar`\_`gc`, `someConstVar`\_`gsc`, `someConstVar`\_`c`, `someColor`\_`gce`, `priv`\_`limit`\_`c`, `pub`\_`maxBufferSize`\_`sc`).
- **Kind markers** — all 8 `pointer` variants (`p`, `pc`, `pv`, `pcv`, `pe`, `pce`, `pve`, `pcve`) and all 8 `reference` variants (`r`, `rc`, `rv`, `rcv`, `re`, `rce`, `rve`, `rcve`, with the [`cv-qualifier`] marker intentionally omitted), the `enum` markers (`e`, `ce`, `ve`, `cve`) for plain-enum and enum-class variables, and the compound forms (`state`\_`gscvpcve`, `state`\_`gsrcve`) combining scope, storage, cv and a pointer or reference to a `const volatile` enum type; the note that the markers apply to smart pointers alike is stated in [Pointer markers](#115-pointer-markers).
- **Array and member-pointer forms** — `TAA_` / `TAM_` aliases and the variable names that go with them, which take no kind marker (`frameBuffer`\_`g`, `offset`\_`g`, `renderHandler`\_`g`), `TAP_` for a pointer to an array, and the `TAA_` / `TAAC_` / `TAAS_` reading rule of [Type alias prefixes](#123-type-alias-prefixes-prefixes-for-types-created-via-usingtypedef-keywords).
- **Local (block) scope** — names with no scope marker (`someVar`, `someVar`\_`s`, `dataBuffer`\_`p`, `logger`\_`p`), a name introduced by a structured binding (`xCoordinate`, `yCoordinate`) with no marker block, and Boolean predicates (`isVisible`).
- **Members** — the access markers `pub_` / `prot_` / `priv_` on plain, pointer, enum, static and `static thread_local` members alike, in `class`, `struct` and `union` types, with `mutable` members following the same naming rules as non-`mutable` ones of the same access level (`pub`\_`accessCount`, modifiable through the `const` method `touch()`); and the access discipline — fields accessed bare (no `this->`), non-static methods via `this->…`, static members and methods via the class name (`C_Logger`::`pub`\_`instanceCount`\_`s`, `C_Logger::resetCount()`, `C_Container`::`pub`\_`sharedCount`\_`s`).
- **Functions and macros** — `camelCase` functions and methods (`sendRequest`, `computeFrameSum`, `logMessage`, `touch`, `resetCount`, `retrieve`, `update`, `refreshState`, `drawContent`; `main` is a name the language fixes — one of the deviations listed in [Scope and permitted deviations](#scope-and-permitted-deviations)), a function with internal linkage declared in an anonymous namespace (`scaleFactorFor`, the same form with no marker), the function-like macro `SAVE_DATA` with bare noun parameters (`destination`, `source`), and the object-like macro `MAX_BUFFER_SIZE`.
- **Types and aliases** — the prefixes `C`, `S`, `E`, `U`, the alias prefixes `TA`, `TAC`, `TAS`, `TAE`, `TAU`, `TAP`, `TAR`, `TAF`, `TAA`, `TAM`, and the enumerator casing (`UPPER_SNAKE_CASE` for a plain `enum` — `STATE_IDLE`, …; `PascalCase` for an `enum class` — `DeepPurple`, …); the role-marked prefixes `IS_`, `AC_`, `PC_`, `PAC_` demonstrated directly (the remaining forms `IC_/AS_/PS_/PAS_` follow from the five-combination marker rule — *(none)*, `I`, `A`, `P`, `PA` — and the clause-based exclusion of `PI_` is stated in [Abstraction & protocol markers](#122-abstraction--protocol-markers)) and the marker-aware aliases (`TAIS_Drawable`; family `TAIC_/TAAC_/TAAS_/TAPC_/TAPS_/TAPAC_/TAPAS_`).
- **Template parameters** — all six kinds (`TTP`, `TTPP`, `NTTP`, `NTTPP`, `TeTP`, `TeTPP`) and the template-class members of `C_Container`.
- **Hierarchies** — static forwarding through a protocol (`ticker.refresh()`, `panel.refresh()`) and virtual dispatch through an interface reference (`drawable_r.draw()`); the mixin over an interface (`PC_DrawMixin`) — a protocol that also implements a dynamic contract, named by the same clauses (`PC_`) and satisfying the destruction rule through the destructor implicitly declared `virtual` because the base's destructor is; and the destruction rule itself — `IS_Drawable` declares a public `virtual` destructor, so objects are destroyed through the interface, while `PC_Refreshable` declares a protected non-virtual one, so deleting through a protocol pointer is a compile error rather than undefined behavior.
