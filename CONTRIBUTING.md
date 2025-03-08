# 🌊 Contributing to Plouf

Thank you for considering contributing to Plouf! I really appreciate your support. 🚀

## How to Contribute

1. **Fork the repository**: Click the "Fork" button at the top right of the repository page.
2. **Clone your fork**: Clone your forked repository to your local machine.
   ```sh
   git clone https://github.com/tristanqtn/Plouf.git
   ```
3. **Create a branch**: Create a new branch for your feature or bugfix.
   ```sh
   git checkout -b my-feature-branch
   ```
4. **Make your changes**: Implement your feature or fix the bug.
5. **Commit your changes**: Commit your changes with a descriptive commit message.
   ```sh
   git add .
   git commit -m "Description of my changes"
   ```
6. **Push to your fork**: Push your changes to your forked repository.
   ```sh
   git push origin my-feature-branch
   ```
7. **Create a Pull Request**: Open a pull request to the main repository. Provide a clear description of your changes and any related issues.

## Code of Conduct

### Our Pledge

In the interest of fostering an open and welcoming environment, we as contributors and maintainers pledge to make participation in our project and our community a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

- The use of sexualized language or imagery and unwelcome sexual attention or advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information, such as a physical or electronic address, without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

### Our Responsibilities

Project maintainers are responsible for clarifying the standards of acceptable behavior and are expected to take appropriate and fair corrective action in response to any instances of unacceptable behavior.

### Scope

This Code of Conduct applies both within project spaces and in public spaces when an individual is representing the project or its community.

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team at [INSERT EMAIL ADDRESS]. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances. The project team is obligated to maintain confidentiality with regard to the reporter of an incident.

### Attribution

This Code of Conduct is adapted from the [Contributor Covenant](https://www.contributor-covenant.org), version 1.4.

## Reporting Issues

If you find a bug or have a feature request, please open an issue on the [issue tracker](https://github.com/tristanqtn/Plouf/issues).

## Style Guide

- Follow the existing code style.
- Write clear and concise commit messages.
- Include comments and documentation where necessary.

## Additional Guidelines

- Use the linter `ruff` to ensure code quality.
- Only include the strictly necessary dependencies.
- For the backend, all tests must pass (`poetry run pytest`).
- For every new feature for the backend, write the tests associated with it.
- Even if you didn't change the Docker part, always check that your feature works in a containerized environment.

**Thank you for contributing!**
