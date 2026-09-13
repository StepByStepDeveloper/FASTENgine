# `TAPAS (C++ Naming Conventions)`

## `1. Identifier markers`

### `1.1. Variable markers`

A variable name is a meaningful noun in `camelCase` followed by a **marker block**: every marker that applies to the variable, written as lowercase letters after a single `_`, in the fixed order below (each marker listed below appears at most once, in the specified order, with the [`cv-qualifier`] marker intentionally absent for references — see the notice below).

- `normal-var` (non-enum and non-pointer and non-reference) variable: `camelCase`\_[`scope`][`storage-class`][`cv-qualifier`]
- `enum-var` variable: `camelCase`\_[`scope`][`storage-class`][`cv-qualifier`][`enum`]
- `pointer-var` variable: `camelCase`\_[`scope`][`storage-class`][`cv-qualifier`][`pointer`]
- `reference-var` variable: `camelCase`\_[`scope`][`storage-class`][`reference`]

Markers are trailing on purpose: the meaningful part of every name comes first, so a reader (and an editor's completion list) sees *what the variable holds* before *how it is qualified*, and no reading order is inverted. A trailing marker block also cannot produce a reserved identifier, because it never contains a double underscore and never places an underscore before an uppercase letter.

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

> Variables declared inside an anonymous (unnamed) namespace have internal linkage by definition — the compiler guarantees this automatically, so there is no need (and it is an error) to additionally apply the `static` (`s`) storage-class marker. The `a` marker is therefore mutually exclusive with the `static` (`s`) and `extern` (`x`) storage-class markers (see the storage-class markers below). An anonymous-namespace variable with internal-linkage storage is written `someVar`\_`a`, never `someVar`\_`as`.

**Important notice for local (function/block) scope**:

> Variables declared inside a function or block scope are *block-scoped*: they have no linkage and are not members of any namespace. They intentionally **omit the [`scope`] marker** entirely — `g`, `n` and `a` describe namespace scope only, so no name of a local variable ever carries one. The marker block of a local variable therefore starts with the [`storage-class`] marker (e.g., a `static` local is `someLocal`\_`s`, a `thread_local` local is `someVar`\_`t`, a `const` local is `someLocal`\_`c`), and a local that has nothing to mark at all is written with no block and no trailing underscore (e.g., `someVar`). Recall that the minimal forms shown in the [Non-Member variable naming conventions](#7-non-member-variable-naming-conventions) table (such as `operatingMode`\_`e`, `dataBuffer`\_`p`) are valid only at local scope.

**Important notice for function parameters**:

> A function parameter is block-scoped exactly like any other local variable, so it omits the [`scope`] marker; and because `static` and `extern` cannot be applied to a parameter, no [`storage-class`] marker can appear on one either. What remains is the [`cv-qualifier`] and kind part of the block, so a pointer parameter is `vertices`\_`p` (never `p_vertices`), while an unqualified one keeps its bare name (`vertexCount`).

#### `1.1.2. Storage-class markers`

- `s`: `static` variable (`s` - `s`tatic)
- `t`: `thread_local` variable (`t` - `t`hread_local)
- `st`: `static` `thread_local` variable (`st` - `s`tatic `t`hread_local)
- `x`: `extern` variable (`x` - e`x`tern)
- `xt`: `extern` `thread_local` variable (`xt` - e`x`tern `t`hread_local)

***Example***: `someVar`\_`st` - `static` `thread_local` variable with name `someVar`

**Important notice for the `s` marker at namespace scope**:

> All namespace-scope variables in C++ inherently have static storage duration. However, the `s` marker at namespace scope (e.g., `someVar`\_`gs` or `someVar`\_`ns`) additionally indicates internal linkage — the variable is declared with the `static` keyword and is visible only within the current translation unit. This is a crucial distinction for large projects with multiple source files. The same reasoning applies to both the `global` (`g`) and the `named` (`n`) scope markers.

**Important notice for the `x` marker**:

> The `x` marker marks a variable that is *declared* in one translation unit and *defined* in another one. The `extern` keyword belongs to that declaration only, but the name does not change among translation units: a variable has exactly one name, so the definition is written with the same marked name (`extern int someVar_gx;` declares it; `int someVar_gx = 42;` defines it). `s` and `x` never combine, because `s` marks a name that only its own translation unit can see, while `x` marks a name another translation unit has to provide — no name can be both, and declaring a `static` variable `extern` fails when the program is linked, not when it is compiled. The `xt` marker is the `thread_local` counterpart and follows the same rule.

***Example 1***: `someVar`\_`gx` - `extern` variable in a `global` namespace with name `someVar` (e.g. declared in this translation unit, defined elsewhere)

***Example 2***: `someVar`\_`nxt` - `extern` `thread_local` variable in a `named` namespace with name `someVar`

#### `1.1.3. CV-qualifier markers`

- `c`: `const` variable (`c` - `c`onst)
- `v`: `volatile` variable (`v` - `v`olatile)
- `cv`: `const` `volatile` variable (`cv` - `c`onst `v`olatile)

***Example***: `someVar`\_`cv` - `const` `volatile` variable with name `someVar`

#### `1.1.4. Enum markers`

- `e`: variable of `enum` or `enum class` type (`e` - `e`num)

***Example***: `someVar`\_`e` - variable of `enum` (or `enum class`) type with name `someVar`

**Rationale for the enum marker**:

> The `e` marker on a variable (e.g., `varName`\_`e`) makes it always possible to recognize that the variable is an enumeration. This is especially important when the variable is of a plain `enum` (not `enum class`), because plain enumerators can be assigned directly as `VAL` instead of `E_EnumType::VAL`. If a reader sees `var = VAL`, they might not realize the variable is an enumeration, because in that representation `VAL` may be taken for some constant rather than an enumerator. The `e` marker (`var_e = VAL`) solves that problem.

#### `1.1.5. Pointer markers`

- `p`: `pointer` to object of `class`/`struct`/`union`/`primitive` type (`p` - `p`ointer)
- `pc`: `pointer` to object of `const` `class`/`struct`/`union`/`primitive` type (`pc` - `p`ointer `c`onst)
- `pv`: `pointer` to object of `volatile` `class`/`struct`/`union`/`primitive` type (`pv` - `p`ointer `v`olatile)
- `pcv`: `pointer` to object of `const` `volatile` `class`/`struct`/`union`/`primitive` type (`pcv` - `p`ointer `c`onst `v`olatile)
- `pe`: `pointer` to object of `enum` (or `enum class`) type (`pe` - `p`ointer `e`num)
- `pce`: `pointer` to object of `const` `enum` (or `enum class`) type (`pce` - `p`ointer `c`onst `e`num)
- `pve`: `pointer` to object of `volatile` `enum` (or `enum class`) type (`pve` - `p`ointer `v`olatile `e`num)
- `pcve`: `pointer` to object of `const` `volatile` `enum` (or `enum class`) type (`pcve` - `p`ointer `c`onst `v`olatile `e`num)

**Important notice for the `pointer` markers**:

> The pointer markers are applicable to smart pointers as well.

***Example***: `someVar`\_`pcve` - `pointer to object of const-volatile-enum type` with name `someVar`

#### `1.1.6. Reference markers`

- `r`: `reference` to object of `class`/`struct`/`union`/`primitive` type (`r` - `r`eference)
- `rc`: `reference` to object of `const` `class`/`struct`/`union`/`primitive` type (`rc` - `r`eference `c`onst)
- `rv`: `reference` to object of `volatile` `class`/`struct`/`union`/`primitive` type (`rv` - `r`eference `v`olatile)
- `rcv`: `reference` to object of `const` `volatile` `class`/`struct`/`union`/`primitive` type (`rcv` - `r`eference `c`onst `v`olatile)
- `re`: `reference` to object of `enum` (or `enum class`) type (`re` - `r`eference `e`num)
- `rce`: `reference` to object of `const` `enum` (or `enum class`) type (`rce` - `r`eference `c`onst `e`num)
- `rve`: `reference` to object of `volatile` `enum` (or `enum class`) type (`rve` - `r`eference `v`olatile `e`num)
- `rcve`: `reference` to object of `const` `volatile` `enum` (or `enum class`) type (`rcve` - `r`eference `c`onst `v`olatile `e`num)

***Example***: `someVar`\_`rcve` - `reference to object of const-volatile-enum type` with name `someVar`

#### `1.1.7. Ultimate variable naming examples`

***Example 1***:

```C++
enum E_DeviceState { STATE_IDLE, STATE_RUNNING, STATE_ERROR };

const volatile E_DeviceState targetState_gcve = STATE_IDLE;

static const volatile E_DeviceState* const volatile someVar_gscvpcve = &targetState_gcve;
```

Variable `someVar`\_`gscvpcve` is `global`-scope, internal-linkage (`static`), `const volatile` pointer to an object of `const-volatile-enum` type, with name `someVar` (`g`lobal `s`tatic `c`onst `v`olatile `p`ointer `c`onst `v`olatile `e`num):

- variable has `global` scope
- variable has internal linkage (`static`)
- variable has `const volatile` qualifiers
- variable has `pointer` type
- variable points to object of `const-volatile-enum` type, specifically `E_DeviceState`

***Example 2***:

```C++
enum E_DeviceState { STATE_IDLE, STATE_RUNNING, STATE_ERROR };

const volatile E_DeviceState targetState_gcve = STATE_IDLE;

static const volatile E_DeviceState& someVar_gsrcve = targetState_gcve;
```

Variable `someVar`\_`gsrcve` is `global`-scope, internal-linkage (`static`) reference to an object of `const-volatile-enum` type, with name `someVar` (`g`lobal `s`tatic `r`eference `c`onst `v`olatile `e`num):

- variable has `global` scope
- variable has internal linkage (`static`)
- variable has `reference` type
- variable refers to object of `const-volatile-enum` type, specifically `E_DeviceState`

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

`Role markers` (normative clauses in [Abstraction & Protocol Markers](#122-abstraction--protocol-markers); the lines below are a summary only):

- *(none)*: concrete type
- `I`: `interface` type — a complete dynamic contract: pure virtual functions only, no data member, destruction through the base is well-defined or impossible to write (`I` - `I`nterface)
- `A`: `abstract` type — a base that is not yet complete: abstract, yet failing at least one `I` clause — typically it carries state or implementation (`A` - `A`bstract)
- `P`: `protocol` type — a compile-time contract on a statically known derived type: a mixin that states what its host owes (`P` - `P`rotocol)

`Role markers` concatenate in the fixed order and admit exactly five combinations: *(none)*, `I`, `A`, `P`, `PA`. In particular, the combination `PI` cannot exist: `P` requires a contract member (clause `P1`), and an interface is forbidden to declare one (clause `I4`).

Resulting prefixes: `C`, `S`, `E`, `U`, `IC`, `IS`, `AC`, `AS`, `PC`, `PS`, `PAC`, `PAS`.

**Important notice for `union` and `enum`**:

> `Role markers` never combine with the `U`/`E` `type letters` — unions cannot declare virtual member functions or participate in inheritance, and enums have no members at all.

#### `1.2.2. Abstraction & Protocol Markers`

Terms used by the clauses below:

- **declared by the type** — written in the type's own definition; **inherited** — brought in with a base class; together they form the type's **member set**. Implicitly-declared special member functions are neither: they appear in no definition, so they never satisfy a clause. `I6` is the exception — it reads the **effective destructor** (the one the type ends up with, declared or implicitly declared), because that is what a `delete` through the type actually runs.
- **own virtual function** — a virtual function declared by the type (an `override` counts; a declared destructor counts; an implicitly-declared virtual destructor does not).
- **special member function** — default constructor, copy/move constructor, copy/move assignment operator, destructor, in any form (defaulted, deleted, pure).
- **data member** — a non-static data member; static data members are not fields and carry no per-object state.
- **contract member** — a member declared by the type that names its derived-type template parameter `TTP_Derived` (a non-static member function, a static member function or a member function template, e.g. `void refresh() { static_cast<TTP_Derived&>(*this).onRefresh(); }`).
- **mixin** — a class template that hands functionality to the class deriving from it, typically through CRTP; a **protocol** is this document's name for the mixin form that obliges its host (see `P` below).
- **abstract** — standard C++ sense: at least one pure virtual function in the member set has no final overrider in the type (`std::is_abstract_v<T>`); otherwise the type is **concrete**.

`Role markers`:

- **`I` (interface)** — a complete dynamic contract:
  1. the type is abstract;
  2. it declares or inherits at least one pure virtual non-special member function;
  3. every non-special member function in its member set is pure virtual;
  4. it declares no contract member;
  5. it has no data member;
  6. destroying an object through the interface is well-defined. Only two destructor forms qualify: a `public` `virtual` destructor, so that `delete` through the interface runs the whole destruction chain, or a destructor that is not `public` (`protected` or `private`), so that `delete` through the interface cannot be written at all. The single forbidden form is a `public` non-`virtual` destructor — declared or implicitly declared — where `delete` through the interface compiles, runs only the base part of the chain and leaves the derived type's own destructor unrun, which is undefined behavior;
  7. static members are permitted and lie outside `I2`, `I3` and `I5`.

  *Consequences*: an interface inherits only from interfaces (`I3` and `I5`) — which admits the *composite* form, an interface that aggregates several contracts and declares nothing of its own (it passes `I2` on what it inherits) — and no helper implementation may be added to one: helpers belong to an abstract type. Clause `I4` is not a matter of taste: a user holding the interface sees exactly its virtual functions, so a member that is not virtual is not part of the contract at all, and an obligation toward a derived type is never visible through the interface.
- **`A` (abstract)** — an incomplete base that exists to be completed:
  1. it is abstract;
  2. it fails at least one `I` clause — that is what distinguishes it from an interface. Any of `I2`–`I6` can be the failing one: most often `I5` (it carries a data member, that is the state its derived types share) or `I3` (it carries an implementation), occasionally `I2` (its member set holds no pure virtual non-special member function — the only pure virtual function it has, if any, is a special member such as a destructor), `I4` (it declares a contract member, which also makes it `PA` — see clause `A3` below) or `I6` (an unsafe destructor). `I1` holds by definition and `I7` only permits, so neither can fail; a type that fails none of `I1`–`I7` is an interface itself;
  3. it declares no contract member (a contract member makes it `PA`);
  4. it states no contract of its own: unlike `I` it is not a complete handle for its users, and unlike `P` it names no obligations for a single derived type. Own pure virtual functions, `override = 0` re-declarations, data members and implementations are otherwise allowed, and whether objects are destroyed through it is left to the destruction rule below.
- **`P` (protocol)** — a compile-time contract on a statically known derived type:
  1. it declares at least one contract member (the derived type passes itself as `TTP_Derived`);
  2. everything else is optional: data members, static members, non-virtual implementations and virtual members are all allowed;
  3. the marker states what the type *requires* of its derived type, not what it *implements* itself: whether a protocol carries a vtable is visible from its declarations, not from its name. A protocol is the contract side of a **mixin** (see *Protocol and mixin* below), and a protocol that also implements a dynamic contract is a **mixin over an interface**, named by these same clauses (`PC_`/`PAC_`); the Guidance below still recommends decomposing it into a dynamic base plus a standalone protocol.

Contract forms:

- An `I` type states a **dynamic** contract: everything a user may do with an object is reachable through the type itself, so every member of the contract is virtual, and the implementor's obligation is to override every pure virtual function — a derived type that leaves one unoverridden stays abstract.
- A `P` type states a **static** contract: the obligations are the members named by its contract members, and they are visible to the compiler only, never through the type — no handle exists over a protocol, and `PC_X<C_A>` and `PC_X<C_B>` are unrelated types.
- Both markers oblige a derived type; they differ in the form of the contract and in what the type gives its users (a handle, or nothing). An `A` type states no contract of its own.

Composition rules:

- `Role markers` concatenate in the fixed order. Exactly five marker combinations exist: *(none)*, `I`, `A`, `P`, `PA`.
- **`I` and `P` are mutually exclusive by clause, not by argument**: `P` requires a contract member (clause `P1`), and an interface is forbidden to declare one (clause `I4`) — `PI` cannot be written.
- **`PA` (`PAC_`, `PAS_`)** is the only hybrid: a protocol that is abstract. Its abstractness may come from a pure virtual function it declares itself or from an inherited pure virtual function it does not override.
- One type bears exactly one resulting prefix; no other combinations exist.

Mechanical classification algorithm:

1. Does the type declare a contract member (a member that names `TTP_Derived`)? If any exist, remember marker `P`.
2. Is the type abstract in the standard C++ sense — at least one pure virtual function (declared by the type or inherited) has no final overrider in it?
   - No → the type is concrete: `PC_`/`PS_` if marker `P` was remembered, otherwise `C_`/`S_`. Implementing every inherited pure virtual function makes a type concrete even though it keeps a vtable (e.g. `C_Button final : public IS_Drawable`).
   - Yes → `PAC_`/`PAS_` if marker `P` was remembered (the contract member already breaks clauses `I3` and `I4`, so there is nothing left to ask); otherwise continue.
3. Are all `I` clauses (`I1`–`I7` above) satisfied?
   - Yes → `IC_`/`IS_`.
   - No → `AC_`/`AS_`.

Additional rules:

- A class implementing every inherited pure virtual function stays concrete and keeps ordinary naming: `C_Button final : public IS_Drawable` (implementations marked `override`).
- **When an obligation is checked** — an interface's obligation is checked wherever the type is used: a derived type that leaves any pure virtual function unoverridden stays abstract, so the first attempt to create an object fails. A protocol's obligation is checked where the contract member is instantiated, i.e. at its first use: a protocol whose contract member is never used checks nothing, and a type that violates it can be declared, instantiated and run. To check a protocol early, either make the contract member virtual (the diagnostic then arrives earlier, though how early depends on the compiler — Clang instantiates a virtual member with the class, GCC when the class is first used and its vtable is needed), or assert the obligation outside the protocol once the derived type is complete (`static_assert(requires (C_Derived& derived_r) { derived_r.onRefresh(); });`), or constrain the point of use with a concept. A `static_assert` inside the protocol's own body does not work: the derived type is still incomplete there, so the assertion fails even for a derived type that provides everything.
- **Destruction rule** — an object is deleted through a pointer or reference to a base only if that base's destructor is `virtual` (declared or implicitly declared); a base that must not be destroyed through itself declares a *protected non-virtual* destructor, so that the mistake is a compile error instead of undefined behavior. Deletion through a base pointer is therefore always either well-defined or impossible to write, and a base is never left with a public non-virtual destructor. A polymorphic base offered for ownership declares a virtual destructor; a protocol that is never owned through itself takes the protected non-virtual form — the `P` marker says nothing about dispatch, so a protocol that carries a vtable follows the ownership rule like any other base. A public non-virtual destructor on a type with virtual functions is a defect, and both GCC and Clang diagnose it (`-Wnon-virtual-dtor`).
- **Template rule** — a class template is classified by its primary definition, and its role must not depend on its template arguments; a template whose role varies with its arguments must be constrained so that the role is fixed.
- **Protocol and mixin** — a protocol *is* a mixin: the class template hands functionality to the class deriving from it (typically through CRTP) and, by the members its contract members call, states what that class owes back. `P` types are therefore a proper subset of mixins — the ones that state obligations — and the marker names the contract side of a mixin, not a different construct. A mixin that requires nothing of its host declares no contract member and is no protocol: it carries no `P` marker and is classified by the ordinary clauses (`C_`/`S_`).
- **Guidance**: prefer decomposing hybrid designs into orthogonal bases — a dynamic base (`IC_`/`AC_`) plus standalone `PC_` mixins — over `PAC_` hierarchies.
- **Variable markers never encode role markers**: the abstraction level and protocol nature of a type are carried by the type name alone (`renderable`\_`p` regardless of whether it points to an `IC_`, `AC_` or `C_` type). Pairing a protocol with a same-named concept (`PC_Drawable` ↔ `concept Drawable`) is recommended; concept naming itself is out of scope of this document.

***Example 1***:

```C++
enum class E_SomeType { Enum1, Enum2};

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

***Example 4***:

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

***Example 5***:

```C++
template <typename TTP_Derived>
class PC_Refreshable                          // protocol class (CRTP mixin)
{
public:
    void refresh() { static_cast<TTP_Derived&>(*this).onRefresh(); }
};

class C_Ticker final : public PC_Refreshable<C_Ticker>
{
public:
    void onRefresh();
};

template <typename TTP_Derived>
class PAC_PanelBase : public IS_Drawable      // abstract protocol: pure virtual + forwarding + field
{
public:
    void draw() const override = 0;
    void refresh() { static_cast<TTP_Derived&>(*this).onRefresh(); }

protected:
    int prot_width;
};

class C_MainPanel final : public PAC_PanelBase<C_MainPanel>
{
public:
    void draw() const override;
    void onRefresh();
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
- `TAIC`: `type` `alias` to some `interface class` type (`TAIC` - `T`ype `A`lias `I`nterface `C`lass)
- `TAAC`: `type` `alias` to some `abstract class` type (`TAAC` - `T`ype `A`lias `A`bstract `C`lass)
- `TAIS`: `type` `alias` to some `interface struct` type (`TAIS` - `T`ype `A`lias `I`nterface `S`truct)
- `TAAS`: `type` `alias` to some `abstract struct` type (`TAAS` - `T`ype `A`lias `A`bstract `S`truct)
- `TAPC`: `type` `alias` to some `protocol class` type (`TAPC` - `T`ype `A`lias `P`rotocol `C`lass)
- `TAPS`: `type` `alias` to some `protocol struct` type (`TAPS` - `T`ype `A`lias `P`rotocol `S`truct)
- `TAPAC`: `type` `alias` to some `abstract protocol class` type (`TAPAC` - `T`ype `A`lias `P`rotocol `A`bstract `C`lass)
- `TAPAS`: `type` `alias` to some `abstract protocol struct` type (`TAPAS` - `T`ype `A`lias `P`rotocol `A`bstract `S`truct)

**Important notice for aliases of aliases**:

> A `using`/`typedef` declaration introduces no new type — an alias is just another name for the underlying type. Therefore, an alias of another alias must be named according to the *resolved* underlying type's category (e.g., aliasing a `TAC_SomeType` still yields a `TAC_…` name, not a separate `TAA` prefix). There is intentionally no `TAA` prefix. The resolved underlying category includes role markers (e.g., aliasing a `PAC_SomeType` yields a `TAPAC_…` name, preserving the `[P][A][kind]` marker order).

***Example 1***:

```C++
enum class E_SomeType { Enum1, Enum2};

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

#### `1.3.2. Non-Type template parameter prefixes`

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

## `3. Namespace naming conventions`

| Entity     | Convention   | Example          |
|:---------- | ------------ | ---------------- |
| Namespaces | `snake_case` | `frame_renderer` |

## `4. Type naming conventions`

| Entity          | Convention                           | Example             |
|:--------------- | ------------------------------------ | ------------------- |
| Type name       | noun in `type-name` style-form       | `C_FrameRenderer`   |
| Type alias name | noun in `type-alias-name` style-form | `TAC_FrameRenderer` |

## `5. Function-like Macro and Function/Method naming conventions`

| Entity                   | Convention                                         | Example         |
|:------------------------ | -------------------------------------------------- | --------------- |
| Function-like macro name | imperative verb in `UPPER_SNAKE_CASE()` style-form | `SAVE_DATA()`   |
| Function/Method name     | imperative verb in `camelCase()` style-form        | `sendRequest()` |

**Important notice for member-method calls**:

> Non-`static` member methods **must** be called from within the class's own methods exclusively via the `this->` qualifier (e.g., `this->resizeBuffer()`). The `this->` qualifier **must never** be omitted so that it is always obvious a call targets an instance method rather than a free function. `static` member methods, conversely, **must** be qualified with the enclosing class name (e.g., `C_SomeType::create()`) and **must never** be called via `this->`. Member *fields* are the exact opposite: they are never accessed through `this->`, because the access marker already identifies them (see [Member variable naming conventions](#8-member-variable-naming-conventions)).

## `6. Object-like Macro and Enumerator naming conventions`

| Entity                              | Convention                                | Example           |
|:----------------------------------- | ----------------------------------------- | ----------------- |
| Object-like macro name              | noun in `UPPER_SNAKE_CASE` style-form     | `MAX_BUFFER_SIZE` |
| Enumerator name for enum-class type | any name in `PascalCase` style-form       | `DeepPurple`      |
| Enumerator name for enum type       | any name in `UPPER_SNAKE_CASE` style-form | `DEEP_PURPLE`     |

**Rationale for enumerator naming**:

> For backward compatibility with C-style conventions, plain `enum` enumerators use `UPPER_SNAKE_CASE` (e.g., `DEEP_PURPLE`). For `enum class` enumerators, the mandatory type-name qualifier `E_EnumType::` allows the enumerator name itself to be written in `PascalCase` instead of `UPPER_SNAKE_CASE`, yielding the full form `E_Color::DeepPurple`.

## `7. Non-Member variable naming conventions`

| Entity                  | Convention                         | Example              |
|:----------------------- | ---------------------------------- | -------------------- |
| Enum variable name      | noun in `enum-var` style-form      | `operatingMode`\_`e` |
| Pointer variable name   | noun in `pointer-var` style-form   | `dataBuffer`\_`p`    |
| Reference variable name | noun in `reference-var` style-form | `dataBuffer`\_`r`    |
| Ordinary variable name  | noun in `normal-var` style-form    | `operatingMode`      |

## `8. Member variable naming conventions`

The base name of a member variable follows the same rules as for non-member variables (a meaningful noun in `camelCase` plus a marker block). On top of that, the requirements below apply.

**Important notice for the access marker and member scope**:

> Every member carries a mandatory **access marker** as its leading prefix — `pub_`, `prot_` or `priv_` — and omits the [`scope`] marker entirely: a member is *class-scoped*, never namespace-scoped, so `g` / `n` / `a` never apply to a field. What follows the base name is the same trailing marker block as for any other variable, i.e. [`access-marker`]\_`camelCase`\_[`storage-class`][`cv-qualifier`][`enum`|`pointer`|`reference`]:
>
> - An ordinary (instance) non-static member carries **no storage-class marker** (e.g., `pub`\_`operatingMode`, `prot`\_`operatingMode`\_`pe`).
> - A `static` class member carries the **`s`** storage-class marker (e.g., `pub`\_`instanceCount`\_`s`). Note carefully: at *namespace* scope `s` means internal linkage, but a `static` class member has **external linkage**. The `s` marker on a member therefore denotes *class-level (shared) storage only*, not internal linkage — there is no contradiction because the scope marker is absent and the class scope, not the storage marker, governs linkage. The `x` (`extern`) marker is **never** used on members: `static` members are defined exactly once and resolved by the linker; a declaration of one is written in the header with the plain `s` marker and defined in one source file with the same `s` marker (the keyword `static` is omitted at the definition).
> - `thread_local` members additionally carry **`t`** (e.g., `prot`\_`threadStorage`\_`t`), and `static thread_local` members carry **`st`** (e.g., `pub`\_`cache`\_`st`), mirroring the namespace-scope storage-class markers.
>
> The access marker is always the leading prefix and the marker block is always trailing; the two never merge, swap places, or absorb one another (see [Members combining the access marker and the marker block](#82-members-combining-the-access-marker-and-the-marker-block)).

Access rules:

- Non-`static` fields declared in a class are accessed **bare** inside the class's own methods (e.g., `operatingMode`). The `this->` qualifier is **forbidden** on fields: the access marker already makes it obvious that the name denotes a class field, so the qualifier adds nothing but noise.
- `static` members are **not** accessed via `this->` (they have no instance). They **must** be qualified with their enclosing class name (e.g., `C_SomeType`::`pub`\_`instanceCount`\_`s`) even from within the class's own methods, so that the access is unambiguously a class-level entity.
- Access from outside the class uses the object or the pointer — `obj`.`pub`\_`operatingMode` and `ptr`->`pub`\_`operatingMode` — once again with the member's full name.

A member's name is identical wherever it is written, inside or outside the class; only the qualifier that selects the object differs:

| Access level | Leading marker | Inside class methods          | Outside the class (via object/pointer)                                                            |
|:------------ |:-------------- |:----------------------------- | ------------------------------------------------------------------------------------------------- |
| `public`     | `pub_`         | `pub`\_`accessCount`          | `obj`.`pub`\_`accessCount` / `ptr`->`pub`\_`accessCount`                                          |
| `protected`  | `prot_`        | `prot`\_`operatingMode`\_`pe` | `obj`.`prot`\_`operatingMode`\_`pe` / `ptr`->`prot`\_`operatingMode`\_`pe` (derived classes only) |
| `private`    | `priv_`        | `priv`\_`targetState`\_`e`    | Not accessible                                                                                    |

### `8.1. mutable members`

The `mutable` keyword is orthogonal to access level and to all marker categories: it governs whether a field may be modified through a `const`-qualified method, not the field's scope, storage, or type. `mutable` members therefore follow exactly the same naming rules as non-`mutable` members of the same access level; the `mutable` qualifier is intentionally not encoded in the name.

***Example***:

```C++
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

A member always carries both mechanisms at once: the access marker as its leading prefix (from the access level) and the marker block as the tail of the base name (from the variable's own storage, qualifiers and type). Neither mechanism is ever folded into the other, and the block keeps the same order it has for a non-member variable.

***Example***:

```C++
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

| Entity                           | Convention                            | Example          |
|:-------------------------------- | ------------------------------------- | ---------------- |
| Type template parameter          | noun in `TTP_PascalCase` style-form   | `TTP_Value`      |
| Type template parameter pack     | noun in `TTPP_PascalCase` style-form  | `TTPP_Args`      |
| Non-type template parameter      | noun in `NTTP_PascalCase` style-form  | `NTTP_Count`     |
| Non-type template parameter pack | noun in `NTTPP_PascalCase` style-form | `NTTPP_Values`   |
| Template template parameter      | noun in `TeTP_PascalCase` style-form  | `TeTP_Allocator` |
| Template template parameter pack | noun in `TeTPP_PascalCase` style-form | `TeTPP_Policies` |

## `10. Ultimate Compilable Example`

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
struct     S_Point       { int pub_x; int pub_y; };                   // struct type
union      U_Packet      { int pub_raw; float pub_floating; };        // union type
class      C_Renderer;                                                // class type (forward)
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

extern int              someVar_gx;                          // extern declaration (defined elsewhere)
extern thread_local int someVar_gxt;                         // extern thread_local declaration

// global enum variables
E_DeviceState                someState_ge     = STATE_IDLE;  // scope = g + enum
const E_DeviceState          someState_gce    = STATE_IDLE;  // g + const + enum
const volatile E_DeviceState targetState_gcve = STATE_IDLE;  // g + const volatile + enum

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
int*                                                intTarget_gp   = &intTarget_g;    // global pointer
const int*                                          intTarget_gpc  = &intTarget_gc;   // global pointer to const
volatile int*                                       intTarget_gpv  = &intTarget_gv;   // global pointer to volatile
const volatile int*                                 intTarget_gpcv = &intTarget_gcv;  // global pointer to const volatile
E_DeviceState*                                      state_gpe      = &state_ge;       // global pointer to enum
const E_DeviceState*                                state_gpce     = &state_gce;      // global pointer to const enum
volatile E_DeviceState*                             state_gpve     = &state_gve;      // global pointer to volatile enum
const volatile E_DeviceState*                       state_gpcve    = &state_gcve;     // global pointer to const volatile enum
static const volatile E_DeviceState* const volatile state_gscvpcve = &state_gcve;     // global static const volatile pointer to const volatile enum

// reference variables — no cv-qualifier marker for references
int&                                 intTarget_gr   = intTarget_g;    // global reference
const int&                           intTarget_grc  = intTarget_gc;   // global reference to const
volatile int&                        intTarget_grv  = intTarget_gv;   // global reference to volatile
const volatile int&                  intTarget_grcv = intTarget_gcv;  // global reference to const volatile
E_DeviceState&                       state_gre      = state_ge;       // global reference to enum
const E_DeviceState&                 state_grce     = state_gce;      // global reference to const enum
volatile E_DeviceState&              state_grve     = state_gve;      // global reference to volatile enum
const volatile E_DeviceState&        state_grcve    = state_gcve;     // global reference to const volatile enum
static const volatile E_DeviceState& state_gsrcve   = state_gcve;     // global static reference to const volatile enum

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

    extern thread_local int someVar_nxt;                 // n + extern declaration (definition is elsewhere) of thread_local variable

    int computeFrameSum(int lhs, int rhs) { return lhs + rhs; }  // function: camelCase
}

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
}

// ============================================================================
// Free function (camelCase) demonstrating local-scope variables
// (block scope: no scope marker; the marker block starts with the storage-class marker)
// ============================================================================
void demonstrateLocals()
{
    int                 someVar      = 0;            // local (no markers)
    static int          someLocal_s  = 0;            // local + static
    thread_local int    someVar_t    = 0;            // local + thread_local
    const int           someLocal_c  = 1;            // local + const
    E_DeviceState       someState_e  = STATE_IDLE;   // local + enum
    const E_DeviceState someState_ce = STATE_IDLE;   // local + const enum
    int*                dataBuffer_p = nullptr;      // local + pointer
    const int&          someVar_rc   = someVar;      // local + reference to const
    E_DeviceState&      someState_re = someState_e;  // local + reference to enum
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
    int*        pub_publicBuffer_p;   // public pointer member: access marker + pointer marker
    static int  pub_instanceCount_s;  // public static member (declaration)

protected:
    int            prot_protectedField;    // protected: access marker only
    E_DeviceState  prot_logState_e;        // protected enum member
    E_DeviceState* prot_operatingMode_pe;  // protected pointer-to-enum member

private:
    int           priv_privateField;   // private: access marker only
    E_DeviceState priv_targetState_e;  // private enum member
    static int    priv_someCounter_s;  // private static member (declaration)

public:
    static inline thread_local int pub_cache_st = 0;  // static thread_local member

    C_Logger()
        : pub_someField(0), pub_accessCount(0), pub_publicBuffer_p(nullptr),
          prot_protectedField(0), prot_logState_e(STATE_IDLE), prot_operatingMode_pe(nullptr),
          priv_privateField(0), priv_targetState_e(STATE_IDLE)
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
    void refresh() { static_cast<TTP_Derived&>(*this).onRefresh(); }

protected:
    ~PC_Refreshable() = default;  // destruction rule: protected non-virtual, so deletion through a protocol pointer cannot be written
};

class C_Ticker final : public PC_Refreshable<C_Ticker>
{
public:
    void onRefresh() {}
};

template <typename TTP_Derived>
class PAC_PanelBase : public IS_Drawable  // abstract protocol: pure virtual + forwarding + field
{
public:
    void draw() const override = 0;
    void refresh() { static_cast<TTP_Derived&>(*this).onRefresh(); }

protected:
    int prot_width;
};

class C_MainPanel final : public PAC_PanelBase<C_MainPanel>
{
public:
    void draw() const override {}
    void onRefresh() { ++prot_width; }
};

template <typename TTP_Derived>
class PC_DrawMixin : public IS_Drawable  // mixin over an interface: static + dynamic contract
{
public:
    void draw() const override { static_cast<const TTP_Derived&>(*this).onDraw(); }
    void refresh() { static_cast<TTP_Derived&>(*this).onRefresh(); }
};

class C_Tile final : public PC_DrawMixin<C_Tile>
{
public:
    void onDraw() const {}
    void onRefresh() {}
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
    C_Container() : prot_value(), prot_state_e(STATE_IDLE), priv_internal(0) {}

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
    static inline int priv_privateTotal_s = 0;  // private static inline member
};

// ============================================================================
// Entry point exercising the runnable surface
// ============================================================================
int main()
{
    C_Logger logger;
    logger.logMessage();                // method (camelCase); calling a non-static method via this->
    logger.touch();
    logger.pub_publicBuffer_p = nullptr;    // public field access from outside (obj.member)
    int v = C_Logger::pub_instanceCount_s;  // static member access qualified by class name
    C_Logger::resetCount();

    C_Logger* logger_p = &logger;       // local pointer variable (block scope: no scope marker)
    logger_p->pub_someField = 0;            // public field access via pointer (ptr->member)

    sendRequest(0);
    frame_renderer::computeFrameSum(1, 2);
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

    (void) v;
    
    return 0;
}
```

This example covers:

- **Anonymous namespace** variables (`a`, `ac`, `ae`, `ap`, `arce` markers) and the mutual exclusion of `a` with `static`.
- **cv-qualifier markers** (`c`, `v`, `cv`) at namespace and local scope.
- **Enum markers** (`e`, `ce`, `cve`) for plain-enum and enum-class variables.
- **Enumerator naming**: `UPPER_SNAKE_CASE` for plain `enum` (`STATE_IDLE`, …) and `PascalCase` for `enum class` (`DeepPurple`, …).
- **Extern declarations** (`gx`, `gxt`, `nxt` markers) marked as declarations only, defined elsewhere.
- **File-name convention** represented by the artifact name `ultimate_example.cpp`.
- **Function-like macro** (`SAVE_DATA()`) and **object-like macro** (`MAX_BUFFER_SIZE`).
- **Functions/methods in `camelCase`** (`sendRequest`, `computeFrameSum`, `logMessage`, `touch`, `resetCount`, `retrieve`, `update`, `main`).
- **Local (block) scope** variables with no scope marker (`someVar`, `someLocal`\_`s`, `dataBuffer`\_`p`, `logger`\_`p`, …).
- **Member access markers**: `pub_` / `prot_` / `priv_`, applied to plain, pointer, enum and static members alike, in `class`, `struct` and `union` types.
- **Member access discipline**: fields accessed bare (no `this->`); non-static methods via `this->…`; static members/methods via `C_Logger`::`pub`\_`instanceCount`\_`s` / `C_Logger::resetCount()` / `C_Container`::`pub`\_`sharedCount`\_`s`.
- **Namespace convention** via the `snake_case` namespace `frame_renderer`.
- **Pointer markers** — all 8 variants (`p`, `pc`, `pv`, `pcv`, `pe`, `pce`, `pve`, `pcve`) and the note that they apply to smart pointers alike.
- **Reference markers** — all 8 variants (`r`, `rc`, `rv`, `rcv`, `re`, `rce`, `rve`, `rcve`), with the [`cv-qualifier`] marker intentionally omitted.
- **Scope markers** (`g`, `n`, `a`) and their omission at local/member scope.
- **Static linkage/storage markers** (`s`, `t`, `st`) at namespace scope and as class members, plus the out-of-line static-member definition pattern (keyword `static` omitted, the name retained unchanged).
- **Static thread_local** namespace (`gst`, `nst` markers) and member (`st`) forms.
- **Type prefixes** (`C`, `S`, `E`, `U`) and **type-alias prefixes** (`TA`, `TAC`, `TAS`, `TAE`, `TAU`, `TAP`, `TAR`, `TAF`).
- **Template parameter prefixes** — all 6 kinds (`TTP`, `TTPP`, `NTTP`, `NTTPP`, `TeTP`, `TeTPP`).
- **Ultimate compound forms** (`state`\_`gscvpcve`, `state`\_`gsrcve`) combining scope + storage + cv + pointer/reference-to-const-volatile-enum.
- **`mutable` members** following the same naming rules as non-`mutable` members of the same access level, modifiable through a `const` method (`touch()`).
- **Role-marker type prefixes** — `IS_`, `AC_`, `PC_`, `PAC_` demonstrated directly (remaining forms `IC_/AS_/PS_/PAS_` follow from the five-combination marker rule: *(none)*, `I`, `A`, `P`, `PA`), including the clause-based classification algorithm and the clause-based exclusion of `PI_` (`P` requires a contract member, clause `I4` forbids one).
- **Marker-aware type aliases** (`TAIS_Drawable`; family `TAIC_/TAAC_/TAAS_/TAPC_/TAPS_/TAPAC_/TAPAS_`).
- **Protocol forwarding** through non-virtual members (`ticker.refresh()`, `panel.refresh()`) alongside virtual dispatch through an interface reference (`drawable_r.draw()`).
- **Mixin over an interface** (`PC_DrawMixin`) — a protocol that also implements a dynamic contract: it is named by the same clauses (`PC_`), and it satisfies the destruction rule through the virtual destructor inherited from `IS_Drawable`; the Guidance below still prefers decomposing it into a dynamic base plus a standalone protocol.
- **Destruction rule** — `IS_Drawable` declares a virtual destructor, so objects are destroyed through the interface; `PC_Refreshable` declares a protected non-virtual one, so deleting through a protocol pointer is a compile error rather than undefined behavior.
