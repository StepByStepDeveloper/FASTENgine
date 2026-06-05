# Naming Conventions

## Naming prefixes

### Variables

Variable names may consist of a combination of prefixes in the following order of these prefix types (each type appears exactly once in the specified order):

[`scope-prefix`][`storage-class-prefix`][`cv-qualifier-prefix`][`enum-prefix` xor `pointer-prefix`]_camelCase

[`scope-prefix`][`storage-class-prefix`][`reference-prefix`]_camelCase

The first line applies to enumeration or pointer variables; the second line applies to reference variables, because references themselves do not carry cv-qualifiers — they bind to variables that do, which is reflected in the **Reference prefixes** section below.

#### Scope prefixes

- g: variable in `global` namespace (`g` - `g`lobal)
- n: variable in `named` namespace (`n` - `n`amed)

Example: `g_someVar` - variable in the `global` namespace with name `someVar`

#### Storage class prefixes

- `s`: `static` variable (`s` - `s`tatic)
- `t`: `thread_local` variable (`t` - `t`hread_local)
- `st`: `static` `thread_local` variable (`st` - `s`tatic `t`hread_local)

Example: `st_someVar` - `static` `thread_local` variable with name `someVar`

#### cv-qualifier prefixes

- `c`: `const` variable (`c` - `c`onst)
- `v`: `volatile` variable (`v` - `v`olatile)
- `cv`: `const` `volatile` variable (`cv` - `c`onst `v`olatile)

Example: `cv_someVar` - `const` `volatile` variable with name `someVar`

#### Enum prefixes

- `e`: variable of `enum` type (`e` - `e`num)

Example: `e_someVar` - variable of `enum` type with name `someVar`

#### Pointer prefixes

- `p`: `pointer` (`p` - `p`ointer)
- `pc`: `pointer` to `const` object (`pc` - `p`ointer `c`onst)
- `pv`: `pointer` to `volatile` object (`pv` - `p`ointer `v`olatile)
- `pcv`: `pointer` to `const` `volatile` object (`pcv` - `p`ointer `c`onst `v`olatile)

Notice: applicable for smart pointers

Example: `pcv_someVar` - `pointer to const-volatile-object` with name `someVar`

#### Reference prefixes

- `r`: `reference` (`r` - `r`eference)
- `rc`: `reference` to `const` object (`rc` - `r`eference `c`onst)
- `rv`: `reference` to `volatile` object (`rv` - `r`eference `v`olatile)
- `rcv`: `reference` to `const` `volatile` object (`rcv` - `r`eference `c`onst `v`olatile)

Example: `rcv_someVar` - `reference to const-volatile-object` with name `someVar`

#### Ultimate variable naming example

Variable `gscvpcv_someVar` is `global static const volatile pointer to const-volatile-object` with name `someVar`:

- variable has `global` scope
- variable has `static` storage class
- variable is of `const volatile` type
- variable has `pointer` type
- data pointed by this variable is of `const volatile` type

### Types

#### Type prefixes

- `C`: `class` (`C` - `C`lass)
- `S`: `struct` (`S` - `S`truct)
- `E`: `enum` or `enum class` (`E` - `E`num)

#### Type alias (`using`/`typedef`) prefixes

- `TA`: some `type` `alias` (`TA` - `T`ype `A`lias)

#### Rationale for type and alias prefixes

The prefixes `C`, `S`, and `E` must be visible in the type name so that, at the point of variable declaration, it is always obvious which C++ category the underlying type belongs to.

Some types may be type aliases atop existing types. This is conveyed by the `TA_` prefix. The reader must understand that although a variable declared as `TA_SomeType someVar` is allowed to omit certain prefixes (so the user does not have to jump to the alias declaration every time and copy the real type’s qualifiers into the variable name), this does **not** mean the variable or object actually lacks those qualifiers (covering all valid cases: cv, ref, ptr, and so on). The reader can always navigate to the variable declaration, notice that it uses an alias, and inspect the alias definition. However, because an alias is itself a type — a “smart” one — and we are allowed not to know what hides underneath, any additional prefixes added to the variable name are applied relative to the qualifiers of the `TA_SomeType` type itself.

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

```cpp
/// File: widget_renderer.cpp
/// Convention: noun in snake_case.cpp style-form

#include <cstddef>
#include <memory>
#include <tuple>

// Namespace naming: snake_case
namespace fast_engine {

// Object-like macro: UPPER_SNAKE_CASE
#define MAX_RENDER_TARGETS 8

// Function-like macro: UPPER_SNAKE_CASE()
#define LOG_CALL(fn) do { fn; } while (0)

// Type alias: TA_PascalCase
using TA_RenderId = std::size_t;

// Enum class: E_Prefix, enumerators PascalCase
enum class E_Color { DeepPurple, SkyBlue };

// Plain enum: E_Prefix, enumerators UPPER_SNAKE_CASE
enum E_Flags { FLAG_NONE = 0, FLAG_VISIBLE = 1 };

// Struct: S_PrefixPascalCase
struct S_Vertex {
    float x{0.0f};
    float y{0.0f};
};

// Template parameters: T_, NT_, TT_
template <typename T_Data,
          std::size_t NT_BufferSize,
          template <typename> class TT_Allocator>
class C_Array {
public:
    // Public member: no suffix
    T_Data* p_buffer{nullptr};

protected:
    // Protected member: suffix _
    std::size_t capacity_{NT_BufferSize};

private:
    // Private member: suffix __
    TT_Allocator<T_Data> allocator__;

public:
    explicit C_Array(std::size_t cap) : capacity_{cap}, allocator__{} {
        // Member access inside methods: mandatory this->
        this->p_buffer = this->allocator__.allocate(this->capacity_);
    }

    // Method: camelCase imperative verb
    void sendData() {
        if (this->p_buffer != nullptr) {
            const std::size_t c_localCount = this->capacity_;
            std::size_t& r_count = this->capacity_;
            LOG_CALL(r_count = c_localCount);
        }
    }
};

// Template parameter pack: TP_
template <typename... TP_Elements>
class C_Bundle {
private:
    std::tuple<TP_Elements...> items__;
};

// Non-type template parameter pack: NTP_
template <std::size_t... NTP_Dims>
constexpr std::size_t multiplyDimensions() {
    return (1 * ... * NTP_Dims);
}

// Template template parameter pack: TTP_
template <template <typename> class... TTP_Policies>
class C_PolicySet {
};

} // namespace fast_engine

// Global-scope variables with scope / storage / cv / pointer / reference prefixes
static int gs_frameCount = 0;
thread_local int gt_threadId = 1;
const int gc_version = 1;
volatile int gv_status = 0;
const volatile int gcv_mode = 0;

int* gp_handle = nullptr;
int const* gpc_handle = nullptr;

int& gr_counter = gs_frameCount;
const int& grc_limit = gc_version;

fast_engine::E_Color ge_currentColor = fast_engine::E_Color::DeepPurple;
fast_engine::E_Flags ge_currentFlags = fast_engine::FLAG_VISIBLE;

// Named-namespace variable: n_ prefix
namespace fast_engine {
    int n_engineId = 42;
}

// Function: camelCase imperative verb
void sendRequest() {
    // Local ordinary variable
    int operatingMode = 1;

    // Local cv-qualified variables
    const int c_operatingMode = 2;
    volatile int v_operatingMode = 3;
    const volatile int cv_operatingMode = 4;

    // Pointer variables
    int* p_mode = &operatingMode;
    int const* pc_mode = &c_operatingMode;

    // Reference variables
    int& r_mode = operatingMode;
    const int& rc_mode = c_operatingMode;

    // Enum variable: e_ prefix
    fast_engine::E_Color e_color = fast_engine::E_Color::SkyBlue;

    LOG_CALL(operatingMode += 1);
}

int main() {
    fast_engine::C_Array<float, 4, std::allocator> arr{4};
    arr.sendData();

    fast_engine::C_Bundle<int, float, double> bundle{};
    constexpr std::size_t dims = fast_engine::multiplyDimensions<2, 3, 4>();
    (void)dims;

    fast_engine::C_PolicySet<std::allocator, std::default_delete> policies{};
    (void)policies;

    sendRequest();
    (void)ge_currentColor;
    (void)ge_currentFlags;
    (void)fast_engine::n_engineId;

    return 0;
}
```
