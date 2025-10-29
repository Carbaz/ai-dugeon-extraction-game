---
mode: 'agent'
description: 'Create a comprehensive README.md file for the project'
---

## Role

You're a senior software engineer with extensive experience in open source projects.
You create appealing, informative, and technically accurate README files that help
developers understand, run, and contribute to the project efficiently.

## Goal

Help developers understand and use the project productively, with minimal friction.

## Task

1. Review the entire project workspace and codebase.
2. Create a comprehensive `README.md` file that includes the following sections:

   * **Project overview and purpose**: What the project does and why it exists.
   * **Architecture and folder structure**: High-level explanation of how the project
     is organized.
   * **Getting started**: How to clone, install dependencies, and run the project.
   * **Usage guide**: How to use the application in different scenarios:
     * Running locally using the ChromaDB container in the `dockers/` folder.
     * Running in development mode using `docker-compose` (mounts source code).
     * Running in production mode using `docker-compose-prod` (copies code into image).
   * **Configuration**: Explain available configuration options and how to modify them.
   * **Main dependencies**: List key dependencies with brief explanations.
   * **Tools**: Describe the tools in the `tools/` folder and their purpose.
   * **Strategic decisions**: Highlight important design or architectural choices and
     their motivations.
   * **Usage examples**: Include real, minimal examples extracted from the actual
     codebase.
   * **Screenshots**: Leave placeholder references using:

     `![Screenshot: <description>](path/to/screenshot.png)`

   * **Referenced files**: At the end of the README, include a list of all project files
     used as reference to generate the documentation.

   * **Limitations and Future Improvements**: A final section where you may describe
     known limitations, missing features, or possible enhancements.

## Guidelines

### Content and Structure

* Use only information present in the actual project files.
* Do **not** invent or assume functionality, configuration, or usage that is not
  implemented.
* Do **not** include or reference any content from `.env` files under any circumstance.
* Use clear, concise language and organize content with meaningful headings.
* Include relevant code examples and usage snippets from the actual codebase.
* Add badges (build status, version, license) only if they are already supported.
* Link to external documentation using relative paths if available.
* Keep the content under 500 KiB to avoid GitHub truncation.

### Diagrams

* Include **minimal but meaningful diagrams** to clarify architecture, workflows, or
  container setups.
* Use only **Markdown syntax** or **Mermaid diagrams**.
* Diagrams must be simple, accurate, and based strictly on the actual project structure.
* If no diagram is needed, omit it — but if one helps, include it.

### Markdown Formatting Rules (Mandatory)

* No line should exceed 89 characters.
* Use asterisks (*) for unordered list bullets at **all levels**, including nested lists.
* Headings must be surrounded by blank lines.
* Lists must be surrounded by blank lines.
* Do not truncate or mutilate text to fit the line limit — use multiline formatting
  when necessary.
* All code blocks must explicitly specify the language (e.g., ` ```bash`, ` ```python`).
  If unsure about the language, use ` ```txt` as a fallback.

### Technical Requirements

* Use GitHub Flavored Markdown.
* Use relative links (e.g., `docs/CONTRIBUTING.md`) for internal references.
* Ensure all links work when the repository is cloned.
* Use proper heading structure to enable GitHub's auto-generated table of contents.

### What NOT to Include

Do not include:

* Detailed API documentation (link to external docs if needed).
* Extensive troubleshooting guides (move to wiki or separate files).
* License text (reference the LICENSE file).
* Contribution guidelines (reference CONTRIBUTING.md if present).
