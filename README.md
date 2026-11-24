# CI/CD Example

Example repository for the Programming Skills: Continuous Integration lab.

The project contains a simple "hello world" function, unit tests, documentation, and scripts for automating common development tasks.

## Lab instructions

This repository accompanies the CI/CD practical session. Follow the separate lab instructions for your chosen CI/CD platform:

- [GitLab CI/CD](GITLAB_INSTRUCTIONS.md)
- [GitHub Actions](GITLAB_INSTRUCTIONS.md)

The repository intentionally does not contain a complete pipeline configuration. You will develop this during the lab.

## Repository structure

| Path | Description |
|---|---|
| `src/` | Python source code |
| `tests/` | Unit tests |
| `scripts/` | Scripts for automating development tasks |
| `docs/` | Sphinx documentation source files |
| `deploy/` | Predefined deployment configuration |
| `pyproject.toml` | Project metadata, dependencies and tool configuration |

## Local development

A local development environment is not required to complete the lab. However, if you wish to run the code and scripts locally, you will need:

- Python 3.13
- pip 25.1 or later
- Bash (for executing the supplied scripts)

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install --group dev
```

## Running the program

```bash
python -m src.example.hello
```

Expected output:

```text
Hello, World!
```

## Automated tasks

The supplied scripts should be executed from the repository root.

### Linting

Check the Python code using Ruff:

```bash
bash scripts/lint.sh
```

### Unit testing

Run the unit tests using pytest:

```bash
bash scripts/test.sh
```

### Build documentation

Generate HTML documentation using Sphinx:

```bash
bash scripts/build_docs.sh
```

The generated documentation can be viewed by opening `docs/build/html/index.html` in a browser.

## CI/CD

The same scripts can be executed locally or within a CI/CD job. This keeps the tasks themselves independent of the CI/CD platform used to automate them.

During the lab, you will configure a pipeline to:

- Run automated code quality checks.
- Run unit tests with Pytest
- Build project documentation.
- Retain generated documentation as an artifact.
- Deploy documentation to Pages.