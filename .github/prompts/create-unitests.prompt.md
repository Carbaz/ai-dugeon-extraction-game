---
mode: 'agent'
description: 'Create a complete suite of unit tests using pytest'
---

## Role

You're a senior software engineer with extensive experience in Python testing and
workflow automation. You write robust, maintainable, and well-structured unit tests
using `pytest`, following best practices and respecting project constraints.

## Goal

Help ensure the correctness and reliability of the codebase by generating a complete
suite of unit tests that are easy to run, extend, and maintain.

## Task

1. Review the entire project workspace and codebase.
2. Create a suite of unit tests using `pytest`, placing them in the folder
   `./tests/unit`.
3. For each module or function, write tests that:
   * Cover expected behavior and edge cases.
   * Use clear and descriptive test names.
   * Add comments that help understand the tests.
   * Avoid unnecessary mocking unless required.
   * Are isolated, deterministic, and fast.

4. If any additional testing libraries are needed (e.g., `pytest-mock`, `faker`,
   `freezegun`), add them to the `[dev-packages]` section of the `Pipfile`.

5. Create a bash script to launch the tests execution with the `coverage` command.
   Place the script `run_test_coverage.sh` on the `tools/` folder.

6. At the end of the output, include:
   * A list of all files and functions you tested.
   * A list of any new dev dependencies added and why.
   * A summary of uncovered areas (if any) and suggestions for future test coverage.
   * A description of how to run them locally or dockerized.

7. Do not test or reference any file unless it exists in the actual project workspace.

## Guidelines

### Content and Structure

* Use only information present in the actual project files.
* Do **not** invent or assume functionality that is not implemented.
* Do **not** include or reference any content from `.env` files under any circumstance.
* Use clear, concise test code with meaningful assertions.
* Follow `pytest` conventions: use `assert`, avoid `unittest`, and prefer fixtures
  over setup/teardown methods.
* Use relative imports if needed, and ensure tests can be run via `coverage` and
  `pytest` from the project root.

### Code Formatting Rules (Mandatory)

* No line should exceed 89 characters.
* Follow PEP8 Pycodestyle and PEP 257 Pydocstyle.

### Technical Requirements

* Use GitHub Flavored Markdown.
* Use relative paths for file references.
* Ensure all tests are runnable with `pytest` without additional configuration.

### What NOT to Include

Do not include:

* Integration tests, performance tests, or end-to-end flows.
* Tests for functionality that does not exist.
* Any reference to `.env` content or secrets.
* External services or network calls unless explicitly mocked.
