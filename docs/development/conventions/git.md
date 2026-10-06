# Git & PR Workflow

## Commit Guidelines

- **Style**: Use Conventional Commits (e.g., `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`).
- **Atomicity**: One commit should do one thing.
- **Messages**: Write clear, imperative-mood messages (e.g., "Add math library" instead of "Added math library").

## Branching Model

- **main**: Production-ready code.
- **develop/***: Temporary branches for specific tasks — development is done on them; they merge into `main` through a pull request.

## Pull Request Process

1. **Self-Review**: Check your own diff before requesting review.
2. **Description**: Clearly explain *what* changed and *why*.
3. **Tests**: Ensure all tests pass locally before submitting.
4. **CI/CD**: All automated checks must pass before merging.

## Conflict Resolution

- Rebase frequently with the target branch to minimize complex merge conflicts.
