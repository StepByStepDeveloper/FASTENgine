# Naming Conventions

| Entity | Convention | Example |
|--------|------------|---------|
| Implementation/Source file | PascalCase.cpp noun | `FrameRenderer.cpp` |
| Header file | PascalCase.h noun | `FrameRenderer.h` |
| Class name | PascalCase noun | `FrameRenderer` |
| Struct name | PascalCase noun | `ProfileInfo` |
| Enum type-name | PascalCase noun | `ColorEnum` |
| Enum value-name | UPPER_SNAKE_CASE | `DEEP_PURPLE` |
| Basic macro | UPPER_SNAKE_CASE noun | `MAX_BUFFER_SIZE` |
| Function-like macro | imperative UPPER_SNAKE_CASE() | `SAVE_DATA()` |
| Function/Method | imperative camelCase() | `sendRequest()` |
| Local/Global compile-time const-variable (constexpr/consteval) | UPPER_SNAKE_CASE noun | `DEFAULT_TIMEOUT` |
| Local non-const-variable | camelCase noun | `userName` |
| Local run-time const-variable | kPascalCase noun | `kUserName` |
| Global non-const-variable | g_camelCase noun | `g_userName` |
| Global run-time const-variable | g_kPascalCase noun | `g_kUserName` |
| Non-const arg/param | camelCase noun | `firstArg` |
| Run-time/Compile-time const-arg | kPascalCase noun | `kSecondArg` |
| Class non-const data member | m_camelCase | `m_bufferSize` |
| Class run-time/compile-time const data member | m_kPascalCase | `m_kBufferSize` |
| Static non-const-variable | s_camelCase | `s_bufferSize` |
| Static run-time/compile-time const-variable | s_kPascalCase | `s_kBufferSize` |
| Namespaces | snake\_case | `fast_engine` |
