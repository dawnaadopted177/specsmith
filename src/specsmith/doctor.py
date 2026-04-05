# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Doctor — check if verification tools are installed locally."""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ToolCheck:
    """Result of checking a single tool."""

    name: str
    category: str
    installed: bool
    version: str = ""


@dataclass
class DoctorReport:
    """Results from doctor checks."""

    checks: list[ToolCheck] = field(default_factory=list)

    @property
    def installed_count(self) -> int:
        return sum(1 for c in self.checks if c.installed)

    @property
    def missing_count(self) -> int:
        return sum(1 for c in self.checks if not c.installed)


def run_doctor(root: Path) -> DoctorReport:
    """Check if verification tools for the project are installed."""
    scaffold_path = root / "scaffold.yml"
    report = DoctorReport()

    if not scaffold_path.exists():
        return report

    import yaml

    from specsmith.config import ProjectConfig
    from specsmith.tools import get_tools

    try:
        with open(scaffold_path) as f:
            raw = yaml.safe_load(f)
        config = ProjectConfig(**raw)
    except Exception:  # noqa: BLE001
        return report

    tools = get_tools(config)

    for category, cmds in [
        ("lint", tools.lint),
        ("typecheck", tools.typecheck),
        ("test", tools.test),
        ("security", tools.security),
        ("build", tools.build),
        ("format", tools.format),
        ("compliance", tools.compliance),
    ]:
        for cmd in cmds:
            tool_name = cmd.split()[0]
            # Pass root so doctor can find tools in the project's .venv
            check = _check_tool(tool_name, category, root=root)
            report.checks.append(check)

    return report


def _check_tool(name: str, category: str, root: Path | None = None) -> ToolCheck:
    """Check if a tool is available on PATH or in the project's .venv."""
    # Handle compound tool names (cargo clippy → cargo)
    exe = name.split()[0] if " " in name else name

    # Some tools are subcommands (dotnet format → dotnet)
    if exe in ("dotnet", "cargo", "go", "flutter", "nx", "turbo"):
        pass  # Use the base command
    elif exe in ("golangci-lint",):
        pass  # Already the executable name

    # 1. Check system PATH
    path = shutil.which(exe)

    # 2. Fall back to project's .venv (projects often don't install tools globally)
    if not path and root is not None:
        for venv_dir in (".venv", "venv", ".env"):
            # POSIX layout: .venv/bin/<exe>
            posix_path = root / venv_dir / "bin" / exe
            # Windows layout: .venv\Scripts\<exe>.exe
            win_path = root / venv_dir / "Scripts" / (exe + ".exe")
            win_path_no_ext = root / venv_dir / "Scripts" / exe
            for candidate in (posix_path, win_path, win_path_no_ext):
                if candidate.exists():
                    path = str(candidate)
                    break
            if path:
                break

    if not path:
        return ToolCheck(name=name, category=category, installed=False)

    # Try to get version
    version = ""
    try:
        result = subprocess.run(
            [path, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            version = result.stdout.strip().split("\n")[0][:80]
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    return ToolCheck(name=name, category=category, installed=True, version=version)
