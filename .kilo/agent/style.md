# Code Style & Patterns

## Overview

Guidelines for maintaining high-quality, consistent C++ code in FASTENgine.

## General Principles

- **Modern C++**: Prefer C++17 or newer features (e.g., `auto`, `constexpr`, structured bindings).
- **Safety**: Avoid raw pointers for ownership; use smart pointers (`std::unique_ptr`, `std::shared_ptr`).
- **RAII**: Resource Acquisition Is Initialization is mandatory.

## Naming Conventions

| Entity | Convention | Example |
|--------|------------|---------|
| Files | snake_case or PascalCase | `engine_core.cpp` / `EngineCore.cpp` |
| Classes/Structs | PascalCase | `Renderer` |
| Functions/Methods | camelCase or snake_case | `renderFrame()` / `render_frame()` |
| Variables | camelCase or snake_case | `deltaTime` / `delta_time` |
| Constants | SCREAMING_SNAKE_CASE | `MAX_BUFFER_SIZE` |

## Formatting

- **Indentation**: 4 spaces (no tabs).
- **Braces**: Egyptian style (open brace on same line) or Allman style (standard for many C++ projects). *[User should specify]*
- **Line Length**: Max 100-120 characters.

## Best Practices

- Use `const` whenever possible.
- Prefer `override` and `final` for virtual functions.
- Avoid `using namespace std;` in headers.
- Minimize use of macros; prefer `constexpr` or inline functions.
