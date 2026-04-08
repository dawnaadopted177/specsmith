# VS Code Extension — specsmith AEE Workbench

The **specsmith AEE Workbench** VS Code extension is the flagship client for specsmith. It provides
AI agent sessions, a 6-tab Settings panel, execution profiles, the AEE workflow phase indicator,
live Ollama management, FPGA/HDL tool support, and full epistemic engineering workflow — all inside
VS Code's secondary sidebar.

**GitHub:** [BitConcepts/specsmith-vscode](https://github.com/BitConcepts/specsmith-vscode)

---

## Requirements

- VS Code 1.85+
- specsmith **v0.3.5+** installed and on PATH
- At least one LLM provider (API key or local Ollama)

```bash
pipx install specsmith                   # install core CLI
pipx inject specsmith anthropic          # + Claude
pipx inject specsmith openai             # + GPT / O-series
pipx inject specsmith google-generativeai  # + Gemini
```

!!! warning "Do not use bare `pip install specsmith`"
    `pip install` without a virtual environment puts specsmith in your active
    Python's Scripts directory. If you have multiple Pythons (Scoop, Conda,
    system) this creates duplicate binaries that VS Code and your terminal may
    resolve differently. **pipx is the only supported install method for VS Code users.**

---

## Installation

From the [GitHub repository](https://github.com/BitConcepts/specsmith-vscode):

```bash
git clone https://github.com/BitConcepts/specsmith-vscode
cd specsmith-vscode
npm install && npm run build
# Press F5 in VS Code to launch the Extension Development Host
```

!!! note "Marketplace"
    The extension will be published to the VS Code Marketplace. Until then, install from source.

---

## First Run

1. Open the **specsmith** Activity Bar icon (left sidebar)
2. Set your API key: `Ctrl+Shift+P → specsmith: Set API Key`
3. Press `Ctrl+Shift+;` or click **+** in Sessions to start a session
4. Select your project folder — the agent starts automatically and runs the start protocol

The **Settings Panel** opens automatically on startup (`Ctrl+Shift+G` to open manually).

---

## AEE Workflow Phase Indicator

The Settings Panel displays a persistent **phase bar** below the header showing:

- **Current phase pill** — emoji + label (e.g. `📋 Requirements`)
- **Phase description** — what this phase accomplishes
- **Readiness %** — how many prerequisite checks pass (e.g. `60% ready · step 3/7`)
- **→ next phase button** — runs `specsmith phase next` in a terminal
- **Phase selector** — jump to any phase directly

The 7 AEE phases:

```
🌱 Inception → 🏗 Architecture → 📋 Requirements → ✅ Test Spec
   → ⚙ Implementation → 🔬 Verification → 🚀 Release
```

From the CLI:
```bash
specsmith phase                    # show current phase + checklist
specsmith phase next               # advance (checks prerequisites)
specsmith phase set implementation # jump to a phase
```

---

## Settings Panel — 6 Tabs

Open with `Ctrl+Shift+G` or the `📖` toolbar icon.

### Tab: Project
- scaffold.yml form: name, type (35 types), description, languages (multi-select chips with filter), VCS platform, spec version
- **Detect Languages** button — scans file extensions and patches scaffold.yml
- **Upgrade spec** button — runs `specsmith upgrade` in terminal
- Save button persists all changes to scaffold.yml

### Tab: Tools
- **FPGA/HDL tools** (21 tools) — vivado, quartus, gtkwave, ghdl, iverilog, verilator, vsg, yosys, nextpnr, symbiyosys, and more
- **Auxiliary disciplines** — add mixed-discipline support (e.g. FPGA + embedded C + Python verification)
- **CI/CD build platforms** — linux, windows, macos, embedded, cloud, FPGA variants (target deploy/test platforms, not the host OS)
- **Installed Ollama models** with Update / Remove buttons
- All saved to `fpga_tools:`, `platforms:` in scaffold.yml

### Tab: Files
- Governance file status table: scaffold.yml, AGENTS.md, REQUIREMENTS.md, TEST_SPEC.md, ARCHITECTURE.md, LEDGER.md
- ✓ / ✗ indicators with line counts
- **Add** buttons for missing files — choose AI-generated or template
- **Open** buttons for existing files

### Tab: Updates & System
- Current vs available specsmith version (fetches from PyPI)
- **Check for Updates** button — queries PyPI API without resetting the active tab
- **Install Update** button — respects `specsmith.releaseChannel` (stable / pre-release)
- After install: button swaps to **↺ Reload Window** automatically
- Last checked timestamp; Ollama version checker
- System info panel (lazy-loaded): OS, CPU, cores, RAM, GPU, disk

### Tab: Actions & AI
- Quick actions grid: audit --fix, validate, doctor, epistemic-audit, stress-test, export, req list, req gaps
- AI Prompt Palette: 10 pre-written prompts sent to the active agent session

### Tab: Execution
- **Execution profile selector** — `🔒 safe` (read-only), `⚙ standard` (default), `🔓 open`, `⚠ admin`
- Profile description updates live as you change the selection
- **Custom overrides**: additional allowed / blocked command prefixes and agent tool blocks
- Changes saved to `execution_profile`, `custom_allowed_commands`, `custom_blocked_commands` in `scaffold.yml`
- **Tool Installer** — scan tools (runs `specsmith tools scan --json --fpga`), show install status, **Install** button for missing tools opens `specsmith tools install <key>` in a terminal

---

## Agent Sessions

Each session is an independent `specsmith run --json-events` process with:

- Conversation history saved to `.specsmith/chat/chat-YYYYMMDD.jsonl`
- Provider and model remembered per project
- Real-time token meter with context fill bar
- Chat history replayed on session re-open (last 40 messages)
- Auto-start protocol on session ready: sync → load AGENTS.md → read LEDGER.md

**Session status icons in the Sessions sidebar:**

- 🟡 Starting — process spawning
- 🟢 Waiting — ready for input
- ⚙ Running (spin) — agent is thinking
- ⚠ Error — check the chat panel for the error message

---

## Model Provider Support

| Provider | Free tier | Notes |
|----------|-----------|-------|
| **Anthropic** | No | Best for requirements engineering |
| **OpenAI** | No | GPT-4o, o3, o4-mini, GPT-4.1 |
| **Google Gemini** | Yes | Free key at aistudio.google.com |
| **Mistral** | Trial credits | Pixtral supports OCR |
| **Ollama** | Yes (local) | GPU-aware; see below |

API keys are stored in the **OS credential store** (Windows Credential Manager / macOS Keychain) via VS Code SecretStorage — never in `settings.json`.

---

## Ollama — Local Models

```bash
# From terminal
specsmith ollama gpu               # detect VRAM tier
specsmith ollama available         # VRAM-filtered catalog
specsmith ollama pull qwen2.5:14b  # download
specsmith ollama suggest requirements  # task-based recommendations
```

From VS Code:

- **Model dropdown** — shows `Installed` and `Available to Download` groups (GPU-VRAM filtered)
- Selecting an undownloaded model triggers download confirmation → progress notification with Cancel
- `Ctrl+Shift+P → specsmith: Select Model for Task` — task-specific model selector

**Context length auto-detection from GPU VRAM:**

| VRAM | Context |
|------|---------|
| < 4 GB | 4K tokens |
| 4–8 GB | 8K tokens |
| 8–16 GB | 16K tokens |
| 16+ GB | 32K tokens |

Override with `specsmith.ollamaContextLength` in VS Code settings.

**Ollama 404 fix:** The extension automatically resolves quantization-suffix mismatches
(e.g. saved `qwen2.5:14b` → installed `qwen2.5:14b-instruct-q4_K_M`) by querying the actual
installed model list before spawning the session.

---

## Chat Features

- **Drag & drop** — drop files or screenshots onto the chat
- **Paste images** — `Ctrl+V` pastes screenshots directly
- **Copy message** — hover any message → `⎘`
- **Edit last message** — hover user message → `✏` → puts back in input
- **Regenerate** — hover agent message → `↺`
- **Export chat** — `⬇` button → saves as Markdown
- **Clear history** — `🗑` button → clears display + JSONL files + agent context
- **Resize input** — drag the teal handle above the input bar (drag up = bigger)
- **@file** — type `@` in empty input to inject a file as context

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+;` | New agent session |
| `Ctrl+Shift+G` | Open Settings Panel |
| `Ctrl+Shift+R` | Quick add requirement |
| `Ctrl+Shift+Q` | Navigate requirements |
| `Enter` | Send message |
| `Shift+Enter` | New line in message |
| `↑` (empty input) | Recall last message |
| `@` (empty input) | Pick file to inject |
| `Escape` | Stop agent |

---

## Configuration

All settings under `specsmith.*` in VS Code Settings (`Ctrl+,`):

| Setting | Default | Description |
|---------|---------|-------------|
| `specsmith.executablePath` | `specsmith` | Path to specsmith CLI |
| `specsmith.defaultProvider` | `anthropic` | Default LLM provider |
| `specsmith.defaultModel` | `` | Default model (blank = provider default) |
| `specsmith.ollamaContextLength` | `0` | Ollama context size (0 = auto-detect from VRAM) |
| `specsmith.autoOpenGovernancePanel` | `true` | Auto-open Settings panel on VS Code start |

---

## Bridge Protocol

The extension communicates with specsmith via `specsmith run --json-events`:

```
specsmith run --json-events --project-dir <dir> --provider <p> --model <m>
        ↑ stdin: user messages (one line each)
        ↓ stdout: JSONL events
```

Event types: `ready`, `llm_chunk`, `tool_started`, `tool_finished`, `tokens`, `turn_done`, `error`, `system`.

All AI logic lives in the Python CLI — the extension is a pure UI layer.

---

## Troubleshooting

**"specsmith not responding"** — The extension probes for specsmith ≥ v0.3.3 across all known paths.
Run `Ctrl+Shift+P → specsmith: Install or Upgrade` or set `specsmith.executablePath`.

**"Ollama 404 — model not installed"** — The model name doesn't match what's installed. Open the
model dropdown and select from the **Installed** group, or `specsmith ollama list`.

**"Ollama not running"** — Start it: `ollama serve` or open the Ollama desktop app.

**API key 401** — Re-enter: `Ctrl+Shift+P → specsmith: Set API Key`.

**API key 429 (quota exceeded)** — Add credits at your provider's billing portal.

---

## Links

- [GitHub: specsmith-vscode](https://github.com/BitConcepts/specsmith-vscode)
- [GitHub: specsmith](https://github.com/BitConcepts/specsmith)
- [specsmith CLI reference](commands.md)
- [Agentic client overview](agent-client.md)
- [AEE Workflow Phases](commands.md#specsmith-phase)
