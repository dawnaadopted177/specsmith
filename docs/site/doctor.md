# Doctor

`specsmith doctor` checks whether the verification tools for your project type are actually installed on your local machine.

## Usage

```bash
specsmith doctor --project-dir ./my-project
```

## What It Checks

Doctor reads `scaffold.yml` to determine the project type, looks up the [Tool Registry](tool-registry.md) for that type, and checks if each tool's executable is available on PATH.

For a `cli-python` project:

```
Doctor — checking 5 tools

  ✓ lint: ruff (ruff 0.4.8)
  ✓ typecheck: mypy (mypy 1.10.0)
  ✓ test: pytest (pytest 9.0.2)
  ✓ security: pip-audit (pip-audit 2.7.3)
  ✓ format: ruff (ruff 0.4.8)

All 5 tools available.
```

For a `cli-rust` project with missing tools:

```
Doctor — checking 6 tools

  ✓ lint: cargo (cargo 1.77.0)
  ✓ typecheck: cargo (cargo 1.77.0)
  ✓ test: cargo (cargo 1.77.0)
  ✗ security: cargo — not found
  ✓ build: cargo (cargo 1.77.0)
  ✓ format: cargo (cargo 1.77.0)

1 tool(s) missing. 5 installed.
```

## When to Use

- **New dev environment** — Run doctor after cloning a specsmith-governed project to see what you need to install.
- **CI debugging** — If CI fails on a tool, check if it's available locally.
- **Onboarding** — Include `specsmith doctor` in your setup instructions.

## Requirements

Doctor requires `scaffold.yml` in the project. If it doesn't exist, doctor reports "No scaffold.yml found" and exits.
