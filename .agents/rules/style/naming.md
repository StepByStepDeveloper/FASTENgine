# Naming Conventions

## Naming prefixes

### Variables

Notice: naming prefixes can be combined in the order `[scope][storage][cv][enum|ptr|ref]_camelCase` (for example `gscvpc_someVar` is `global static const volatile pointer to const-data` variable with name `someVar`)

#### Scope prefixes

- `g`: `global` variable (`g` - `g`lobal)
- `n`: `namespace` variable (`n` - `n`amespace)

Example: `g_someVar` - `global` variable with name `someVar`

#### Storage class prefixes

- `s`: `static` variable (`s` - `s`tatic)
- `t`: `thread_local` variable (`t` - `t`hread_local)

Example: `gs_someVar` - `global static` variable with name `someVar`

#### cv-qualifier prefixes

- `c`: `const` variable (`c` - `c`onst)
- `v`: `volatile` variable (`v` - `v`olatile)
- `cv`: `const` `volatile` variable (`cv` - `c`onst `v`olatile)

Example: `gsc_someVar` - `global static const` variable with name `someVar`

#### Enum prefixes

- `e`: `enum` variable (`e` - `e`num)

Example: `gsce_someVar` - `global static const enum` variable with name `someVar`

#### Pointer prefixes

- `p`: `pointer` (`p` - `p`ointer)
- `pc`: `pointer` to `const` object (`pc` - `p`ointer `c`onst)

Notice: applicable for smart pointers

Example: `gscpc_someVar` - `global static const pointer to const-data` variable with name `someVar`

#### Reference prefixes

- `r`: `reference` (`r` - `r`eference)

Example: `gscr_someVar` - `global static const reference` variable with name `someVar`

### Types

#### Type prefixes

- `C`: `class` (`C` - `C`lass)
- `S`: `struct` (`S` - `S`truct)
- `E`: `enum` or `enum class` (`E` - `E`num)

#### Type alias (`using`/`typedef`) prefixes

- `TA`: some `type` `alias` (`TA` - `T`ype `A`lias)

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

## Non-Member variable naming conventions

| Entity                  | Convention                                                | Example           |
|:----------------------- | --------------------------------------------------------- | ----------------- |
| Enum variable name      | noun in `[scope][storage][cv][enum]_camelCase` style-form | `e_operatingMode` |
| Pointer variable name   | noun in `[scope][storage][cv][ptr]_camelCase` style-form  | `p_operatingMode` |
| Reference variable name | noun in `[scope][storage][cv][ref]_camelCase` style-form  | `r_operatingMode` |
| Ordinary variable name  | noun in `[scope][storage][cv]_camelCase` style-form       | `operatingMode`   |

## Member variable naming conventions

| Entity                                           | Convention                                                          | Example                |
|:------------------------------------------------ | ------------------------------------------------------------------- | ---------------------- |
| Public member variable name (Vers. 1)            | noun in `this->[non-member-variable-naming-convention]` style-form  | `this->operatingMode`  |
| Public member variable name (Vers. 2)            | noun in `obj->[non-member-variable-naming-convention]` style-form   | `obj->operatingMode`   |
| Public member variable name (Vers. 3)            | noun in `obj.[non-member-variable-naming-convention]` style-form    | `obj.operatingMode`    |
| Protected/Private member variable name (Vers. 1) | noun in `this->[non-member-variable-naming-convention]_` style-form | `this->operatingMode_` |
| Protected/Private member variable name (Vers. 2) | noun in `obj->[non-member-variable-naming-convention]_` style-form  | `obj->operatingMode_`  |
| Protected/Private member variable name (Vers. 3) | noun in `obj.[non-member-variable-naming-convention]_` style-form   | `obj.operatingMode_`   |

## Template parameter naming conventions

| Entity                  | Convention                                                  | Example               |
|:----------------------- | ----------------------------------------------------------- | --------------------- |
| Template parameter name | noun in `[template-parameter-prefix]_PascalCase` style-form | `NTP_GreenVegetables` |
