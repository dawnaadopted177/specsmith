# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Shell tool — execute commands with structured exit code + output."""

from __future__ import annotations

import platform
import subprocess
from pathlib import Path
from typing import Annotated


def run_project_command(
    command: Annotated[str, "Shell command to execute"],
    working_dir: Annotated[str, "Working directory relative to project root"] = ".",
    timeout: Annotated[int, "Timeout in seconds"] = 120,
    project_dir: str = ".",
) -> str:
    """Execute a shell command in the project. Returns [exit N] + output."""
    root = Path(project_dir).resolve()
    cwd = (root / working_dir).resolve()
    try:
        cwd.relative_to(root)
    except ValueError:
        return f"[ERROR] working_dir '{working_dir}' is outside the project directory."

    timeout = min(timeout, 300)
    is_win = platform.system() == "Windows"
    shell_cmd: list[str] = (
        ["powershell", "-NoProfile", "-NonInteractive", "-Command", command]
        if is_win
        else ["bash", "-c", command]
    )

    try:
        result = subprocess.run(  # noqa: S603
            shell_cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=str(cwd),
            timeout=timeout,
        )
        output = (result.stdout + result.stderr).strip()
        if len(output) > 12000:
            output = output[:12000] + f"\n...(truncated, {len(output)} total chars)"
        rc = result.returncode
        return f"[exit {rc}]\n{output}" if output else f"[exit {rc}]"
    except subprocess.TimeoutExpired:
        return f"[TIMEOUT] Command exceeded {timeout}s"
    except FileNotFoundError:
        # Shell not found — fallback to shell=True
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=str(cwd),
                timeout=timeout,
                shell=True,  # noqa: S602
            )
            output = (result.stdout + result.stderr).strip()
            rc = result.returncode
            return f"[exit {rc}]\n{output}" if output else f"[exit {rc}]"
        except Exception as e2:  # noqa: BLE001
            return f"[ERROR] {e2}"
    except Exception as e:  # noqa: BLE001
        return f"[ERROR] {e}"
