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

### Enum variable prefixes

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
- `gscr_`: `global` scope `static` `constexpr` `reference`, can only refer to an object that is usable in constant expressions (`gscr` - global static constexpr reference)
- `nscr_`: `namespace` scope `static` `constexpr` `reference`, can only refer to an object that is usable in constant expressions (`nscr` - namespace static constexpr reference)

### Function parameter prefixes

- `f_`: `function` parameter (`f` - func-param)
- `cf_`: `const` `function` parameter (`cf` - const func-param)
- `pf_`: `pointer` `function` parameter (`pf` - pointer func-param)
- `pcf_`: `pointer` to `const` object `function` parameter (`pcf` - pointer const func-param)
- `cpf_`: `const` `pointer` `function` parameter (`cpf` - const pointer func-param)
- `cpcf_`: `const` `pointer` to `const/constexpr` object `function` parameter (`cpcf` - const pointer const func-param)
- `rf_`: `reference` `function` parameter (`rf` - reference func-param)
- `rcf_`: `reference` to `const/constexpr` object `function` parameter (`rcf` - reference const func-param)
- `ef_`: `enum` `function` parameter (`ef` - enum func-param)
- `cef_`: `const` `enum` `function` parameter (`cef` - const enum func-param)

### Type prefixes

- `C_`: `class` (`C` - Class)
- `S_`: `struct` (`S` - Struct)
- `E_`: `enum` or `enum class` (`E` - Enum)

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

| Entity                          | Convention                          | Example              |
|:------------------------------- | ----------------------------------- | -------------------- |
| Implementation/Source file name | noun in `snake_case.cpp` style-form | `frame_renderer.cpp` |
| Header file name                | noun in `snake_case.hpp` style-form | `frame_renderer.hpp` |

## Namespaces

| Entity     | Convention  | Example       |
|:---------- | ----------- | ------------- |
| Namespaces | snake\_case | `fast_engine` |

## Types

| Entity          | Convention                                          | Example           |
|:--------------- | --------------------------------------------------- | ----------------- |
| Type name       | noun in `[type-prefix]_PascalCase` style-form       | `C_FrameRenderer` |
| Type alias name | noun in `[type-alias-prefix]_PascalCase` style-form | `TA_ProfileInfo`  |

## Functions/Methods

| Entity                   | Convention                                                 | Example            |
|:------------------------ | ---------------------------------------------------------- | ------------------ |
| Function-like macro name | imperative verb in `[macro-prefix]_camelCase()` style-form | `macro_saveData()` |
| Function/Method name     | imperative verb in `camelCase()` style-form                | `sendRequest()`    |

## Constants

| Entity                              | Convention                                           | Example                 |
|:----------------------------------- | ---------------------------------------------------- | ----------------------- |
| Object-like macro name              | noun in `[macro-prefix]_UPPER_SNAKE_CASE` style-form | `macro_MAX_BUFFER_SIZE` |
| Enumerator name for enum-class type | any name in `UPPER_SNAKE_CASE` style-form            | `E_Color::DEEP_PURPLE`  |
| Enumerator name for enum type       | any name in `enum_UPPER_SNAKE_CASE` style-form       | `enum_DEEP_PURPLE`      |

## Variables

| Entity                                                                                         | Convention                                                 | Example               |
|:---------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | --------------------- |
| Enum variable name                                                                             | noun in `[enum-variable-prefix]_camelCase` style-form      | `gsce_operatingMode`  |
| Pointer variable name                                                                          | noun in `[pointer-prefix]_camelCase` style-form            | `gscpc_userName`      |
| Reference variable name                                                                        | noun in `[reference-prefix]_camelCase` style-form          | `gscr_userName`       |
| Function/Method parameter name                                                                 | noun in `[function-parameter-prefix]_camelCase` style-form | `cpcf_someArg`        |
| Local && non-func-param && non-const && non-reference && non-pointer && non-enum variable name | noun in `camelCase` style-form                             | `userName`            |
| Other variable name                                                                            | noun in `[variable-prefix]_camelCase` style-form           | `gsc_userName`        |
| Enum class member variable name                                                                | noun in `[enum-variable-prefix]_camelCase_` style-form     | `gsce_operatingMode_` |
| Pointer class member variable name                                                             | noun in `[pointer-prefix]_camelCase_` style-form           | `gscpc_userName_`     |
| Reference class member variable name                                                           | noun in `[reference-prefix]_camelCase_` style-form         | `gscr_userName_`      |
| Non-const && non-reference && non-pointer && non-enum class member variable name               | noun in `camelCase_` style-form                            | `userName_`           |
| Other class member variable name                                                               | noun in `[variable-prefix]_camelCase_` style-form          | `gsc_userName_`       |
| Enum struct member variable name                                                               | noun in `[enum-variable-prefix]_camelCase` style-form      | `gsce_operatingMode`  |
| Pointer struct member variable name                                                            | noun in `[pointer-prefix]_camelCase` style-form            | `gscpc_userName`      |
| Reference struct member variable name                                                          | noun in `[reference-prefix]_camelCase` style-form          | `gscr_userName`       |
| Non-const && non-reference && non-pointer && non-enum struct member variable name              | noun in `camelCase` style-form                             | `userName`            |
| Other struct member variable name                                                              | noun in `[variable-prefix]_camelCase` style-form           | `gsc_userName`        |

## Template parameters

| Entity                  | Convention                                                  | Example               |
|:----------------------- | ----------------------------------------------------------- | --------------------- |
| Template parameter name | noun in `[template-parameter-prefix]_PascalCase` style-form | `NTP_GreenVegetables` |

## Examples

### Variables and Scopes

```cpp
// Global scope (outside any namespace)
int g_globalCount = 0;
const int gc_globalConst = 100;
static const int gsc_globalStaticConst = 200;

namespace fast_engine {

namespace renderer {
    // Namespace scope
    int n_namespaceVar = 42;
    const int nc_namespaceConst = 100;
    static int ns_namespaceStatic = 7;
}

class C_Renderer {
public:
    void update() {
        // Local variables
        int userName = 0;
        const int c_maxFrames = 1000;
        static int s_counter = 0;
        static const int sc_limit = 5000;

        s_counter++;
    }
};

} // namespace fast_engine
```

### Pointers and References

```cpp
namespace fast_engine {

class C_Object {};

void processData(int f_param, const int cf_param, int* pf_ptr, 
                 const int* pcf_ptr, int& rf_ref, const int& rcf_ref) {
    // Implementation...
}

void pointerExample() {
    C_Object obj;
    
    C_Object* p_obj = &obj;                           // pointer: p_camelCase
    const C_Object* pc_ptrToConst = &obj;             // pointer to const: pc_camelCase
    C_Object* const cp_constPtr = &obj;               // const pointer: cp_camelCase
    const C_Object* const cpc_constPtrToConst = &obj; // const pointer to const: cpc_camelCase

    static C_Object* sp_staticPtr = &obj;                             // static pointer: sp_camelCase
    static const C_Object* spc_staticPtrToConst = &obj;               // static pointer to const: spc_camelCase
    static C_Object* const scp_staticConstPtr = &obj;                 // static const pointer: scp_camelCase
    static const C_Object* const scpc_staticConstPtrToConst = &obj;   // static const pointer to const: scpc_camelCase

    C_Object& r_ref = obj;                            // reference: r_camelCase
    const C_Object& rc_refToConst = obj;              // reference to const: rc_camelCase

    static C_Object& sr_staticRef = obj;                              // static reference: sr_camelCase
    static const C_Object& src_staticRefToConst = obj;                // static reference to const: src_camelCase
}

} // namespace fast_engine
```

### Enums and Types

```cpp
namespace fast_engine {

enum class E_Color { RED, BLUE };                 // enum class type: E_PascalCase, enumerator: UPPER_SNAKE_CASE

enum E_MyEnum { enum_VAL1, enum_VAL2 };           // enum type: E_PascalCase, enumerator: enum_UPPER_SNAKE_CASE

struct S_Transform {                              // struct: S_PascalCase
    float x, y, z;
};

class C_FrameRenderer {                           // class: C_PascalCase
public:
    void render() {}                              // method: camelCase
    static E_Color se_colorType_;                 // enum class member variable (with _): se_camelCase_
};

struct S_TransformWithEnum {                      // struct: S_PascalCase
    float x, y, z;
    static E_Color se_colorType;                  // enum struct member variable (without _): se_camelCase
};

using TA_ProfileInfo = int;                       // type alias: TA_PascalCase

E_MyEnum ne_namespaceEnum;                        // namespace enum variable: ne_camelCase (inside namespace)

void callEnumExample() {
    const E_Color ce_constEnum = E_Color::RED;    // const enum variable: ce_camelCase
    ne_namespaceEnum = enum_VAL1;                 // namespace enum variable: ne_camelCase (inside namespace)
}

} // namespace fast_engine
```

### Macros and Templates

```cpp
#define macro_MAX_BUFFER_SIZE 1024                // object-like macro: macro_UPPER_SNAKE_CASE
#define macro_calculateSum(a, b) ((a) + (b))      // function-like macro: macro_camelCase()

namespace fast_engine {

template <typename T_ValueType>                   // type template parameter: T_PascalCase
class C_Container {
    T_ValueType data_;
};

template <int NT_BufferSize>                      // non-type template parameter: NT_PascalCase
class C_Buffer {};

template <int... NTP_Sizes>                       // non-type template parameter pack: NTP_PascalCase
class C_MultiBuffer {};

template <typename... TP_Args>                    // type pack template parameter: TP_PascalCase
void processPack(TP_Args... args) {}

template <typename T_ValueType, template <typename> class TT_TemplateParam> // template template parameter: TT_PascalCase
class C_NestedContainer {
    T_ValueType data_;
    TT_TemplateParam<T_ValueType> nestedData_;
};

void callMacroExample() {
    int sum = macro_calculateSum(10, 20);
    int size = macro_MAX_BUFFER_SIZE;
}

} // namespace fast_engine
```
