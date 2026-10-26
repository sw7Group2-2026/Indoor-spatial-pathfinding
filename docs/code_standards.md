[← Back to project README](../README.md)

# Python Code Standards

This project uses Python and follows [PEP 8](https://peps.python.org/pep-0008/) naming conventions.

## Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Classes | PascalCase (CapWords) | `UserManager` |
| Files / Modules | snake_case | `user_manager.py` |
| Packages | lowercase | `services` |
| Functions / Methods | snake_case | `get_user_data()` |
| Variables / Attributes | snake_case | `user_name` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES` |
| Internal Methods / Attributes | Leading underscore | `_validate_user()` |

## General notes

- Each file contains an init file to mark it as a python package, for easy importing.
- Be careful when adding stuff to the python init file, since it executes everytime you import it.
- An internal method or attribute is defined within a class and intended to be used internally rather than accessed from outside the class.
- When possible. Try to use design patterns from [Refactoring Guru](https://refactoring.guru/design-patterns)

## Project Structure
This is inspired by object oriented principles.

- Prefer one main class per file.
- Name the file after its class using snake_case.
- Group related modules into packages.
- Small helper classes may share a file when appropriate.


## References

- [PEP 8 – Python Style Guide](https://peps.python.org/pep-0008/)
- [Python Project Layouts – Real Python](https://realpython.com/python-application-layouts/)
  