# Importing Existing Projects

## Overview

`specsmith import` is for projects that already exist but don't have specsmith governance. It walks the directory, detects the project structure, and generates governance files as an overlay — without modifying your source code.

## The Three Phases

### Phase 1: Detection

The importer walks the project tree (skipping `.git/`, `node_modules/`, `__pycache__/`, `build/`, `dist/`, `target/`, `.venv/`) and detects:

**Language detection** — Counts file extensions and maps them to languages. The most frequent language becomes the primary. Supports: Python, Rust, Go, C, C++, C#, JavaScript, TypeScript, JSX, TSX, Java, Kotlin, Swift, Dart, VHDL, Verilog, SystemVerilog, Terraform, Bitbake, Protobuf, GraphQL, LaTeX, Markdown, reStructuredText, KiCad.

**Build system detection** — Checks for marker files at the project root: `pyproject.toml` → pyproject, `Cargo.toml` → cargo, `go.mod` → go-modules, `package.json` → npm, `CMakeLists.txt` → cmake, `west.yml` → west (Zephyr), `build.gradle.kts` → gradle, `pubspec.yaml` → flutter, `*.csproj`/`*.sln` → dotnet, `Makefile` → make.

**Test framework** — `conftest.py` or `pytest.ini` → pytest, `jest.config.*` → jest, `vitest.config.*` → vitest, `Cargo.toml` → cargo-test, `tests/` directory → pytest (for Python).

**CI detection** — `.github/workflows/` → github, `.gitlab-ci.yml` → gitlab, `bitbucket-pipelines.yml` → bitbucket, `Jenkinsfile` → jenkins, `.circleci/` → circleci, `.travis.yml` → travis.

**VCS remote** — Runs `git remote get-url origin` and infers: github.com → github, gitlab → gitlab, bitbucket → bitbucket.

**Existing governance** — Checks for AGENTS.md, LEDGER.md, CLAUDE.md, GEMINI.md, docs/REQUIREMENTS.md, docs/TEST_SPEC.md, docs/architecture.md.

**Modules** — Python: `src/*/` with `__init__.py`. Rust: `src/lib.rs`, `src/main.rs`. Go: directories with `.go` files. JS/TS: `src/*/` subdirectories.

**Entry points** — `src/*/cli.py`, `src/*/__main__.py`, `manage.py`, `app.py`, `main.py`, `src/main.rs`, `cmd/*/main.go`, `src/index.ts`.

**Test files** — Files matching `test_*`, `*_test.*`, `*.test.*`, `*.spec.*`, or in `tests/`/`test/` directories.

### Phase 2: Scaffold Overlay (Merge)

The overlay generates **only what's missing**. If your project already has `AGENTS.md`, it won't be touched. If it has `LEDGER.md` but no `REQUIREMENTS.md`, only REQUIREMENTS.md gets created.

**Files generated:**

- `AGENTS.md` — project name, detected language/build/test info, workflow rules
- `LEDGER.md` — initial import entry with date, type, language
- `docs/REQUIREMENTS.md` — one REQ per detected module + build requirement
- `docs/TEST_SPEC.md` — one TEST per detected test file, linked to module REQs
- `docs/architecture.md` — overview, modules, entry points, language distribution
- `docs/governance/*.md` — six modular governance stubs
- `scaffold.yml` — full ProjectConfig for future specsmith commands
- **CI config** — if no CI detected and VCS platform known, generates tool-aware CI

### Phase 3: AI Enrichment

After import, `AGENTS.md` contains: *"This project was imported by specsmith. The governance files contain detected structure. Review and enrich with your agent."* The AI agent reads this and knows to propose deeper analysis.

## Type Inference Logic

| Condition | Inferred Type |
|-----------|--------------|
| Primary language = VHDL/Verilog/SystemVerilog | `fpga-rtl` |
| Primary language = Bitbake or build = bitbake | `yocto-bsp` |
| Primary language = KiCad | `pcb-hardware` |
| Primary language = Rust, has `src/lib.rs` | `library-rust` |
| Primary language = Rust, has `src/main.rs` | `cli-rust` |
| Primary language = Go | `cli-go` |
| Primary language = C/C++, build = west | `embedded-hardware` |
| Primary language = C/C++, build = cmake, has "lib" module | `library-c` |
| Primary language = C/C++, build = cmake | `cli-c` |
| Primary language = C/C++ (other) | `embedded-hardware` |
| Primary language = C# | `dotnet-app` |
| Primary language = Dart/Swift/Kotlin | `mobile-app` |
| Primary language = Terraform | `devops-iac` |
| Primary language = LaTeX | `research-paper` |
| Primary language = Protobuf/GraphQL | `api-specification` |
| Primary language = JS/TS, package.json has react/vue/angular | `web-frontend` |
| Primary language = JS/TS, has server directory | `fullstack-js` |
| Primary language = Python, has `cli.py` entry point | `cli-python` |
| Primary language = Python, has `manage.py` | `backend-frontend` |
| Primary language = Python, has notebooks/data dirs | `data-ml` |
| Primary language = Python, build = pyproject/setuptools | `library-python` |
| Fallback | `cli-python` |

## Using `--force`

Without `--force`, existing files are never overwritten. With `--force`, all governance files are regenerated from detection results — useful if you want a clean restart of governance on an existing project.

## Using `--guided`

After the overlay is generated, `--guided` runs an interactive architecture session: you name your components, and specsmith generates richer REQUIREMENTS.md (two REQs per component) and TEST_SPEC.md (linked tests) and architecture.md (component descriptions).
