# Code Patterns & Principles

## General Principles

- **Modern C++**: Prefer C++17 or newer features (e.g., `auto`, `constexpr`, structured bindings).
- **Safety**: Avoid raw pointers for ownership; use smart pointers (`std::unique_ptr`, `std::shared_ptr`).
- **RAII**: Resource Acquisition Is Initialization is mandatory.

## Best Practices

- Use `const` whenever possible.
- Avoid `using namespace std;` in headers.
- Minimize use of macros; prefer `constexpr` or inline functions.
- Use enum-classes instead traditional enums.
- **Strict Rule**: Throwing exceptions is strictly forbidden. Use error codes or other non-exception-based error handling mechanisms (e.g., `std::optional`, `std::expected`).

## Polymorphism

Static polymorphism is preferred over dynamic polymorphism. Dynamic polymorphism is only permitted when static polymorphism is difficult or impractical to implement.

**Strict Rules:**

- **NO virtual functions.**
- **NO abstract classes or interfaces (interface classes).**
- **NO `dynamic_cast`.**

### Allowed Mechanisms

#### Static Polymorphism (Preferred)

- **Function Overloading**
- **Operator Overloading**
- **Function Templates**
- **Class Templates**
- **CRTP (Curiously Recurring Template Pattern)**
- **Mixins**
- **Template Specialization** (Full and Partial)
- **`if constexpr` with templates** (C++17)
- **Concepts** (C++20)
- **SFINAE** (fallback for older standards)

#### Dynamic Polymorphism (Without Virtual Functions)

- **Type Erasure** (e.g., `std::function`, custom implementations)
- **`std::variant` + `std::visit`** (C++17)
- **Function pointers / Dispatch tables**
