# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Git tools — structured git operations."""

from __future__ import annotations

import subprocess
from typing import Annotated


def _git(args: list[str], cwd: str, timeout: int = 15) -> str:
    """Run a git command and return stdout, or an error string."""
    try:
        result = subprocess.run(  # noqa: S603, S607
            ["git", "--no-pager", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=cwd,
            timeout=timeout,
        )
        output = (result.stdout + result.stderr).strip()
        if result.returncode != 0:
            return f"[exit {result.returncode}] {output}"
        return output or "(no output)"
    except FileNotFoundError:
        return "[ERROR] git not found on PATH"
    except subprocess.TimeoutExpired:
        return f"[TIMEOUT] git {' '.join(args)} exceeded {timeout}s"
    except Exception as e:  # noqa: BLE001
        return f"[ERROR] {e}"


def git_status(project_dir: str = ".") -> str:
    """Return ``git status --short`` output."""
    result = _git(["status", "--short"], cwd=project_dir)
    return result if result.strip() else "(clean — no uncommitted changes)"


def git_diff(
    staged: Annotated[bool, "If True, show staged changes only"] = False,
    project_dir: str = ".",
) -> str:
    """Return ``git diff`` output (or ``git diff --cached`` for staged)."""
    args = ["diff", "--cached"] if staged else ["diff"]
    return _git(args, cwd=project_dir, timeout=30)


def git_changed_files(project_dir: str = ".") -> str:
    """List files changed since last commit (staged + unstaged)."""
    staged = _git(["diff", "--cached", "--name-only"], cwd=project_dir)
    unstaged = _git(["diff", "--name-only"], cwd=project_dir)
    untracked = _git(["ls-files", "--others", "--exclude-standard"], cwd=project_dir)
    parts: list[str] = []
    if staged and not staged.startswith("["):
        parts.append(f"Staged:\n{staged}")
    if unstaged and not unstaged.startswith("["):
        parts.append(f"Unstaged:\n{unstaged}")
    if untracked and not untracked.startswith("["):
        parts.append(f"Untracked:\n{untracked}")
    return "\n".join(parts) if parts else "(no changes)"


def git_branch_info(project_dir: str = ".") -> str:
    """Return current branch, recent commits, and remote tracking info."""
    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=project_dir)
    log = _git(["log", "--oneline", "-5"], cwd=project_dir)
    remote = _git(["remote", "-v"], cwd=project_dir)
    return f"Branch: {branch}\n\nRecent commits:\n{log}\n\nRemotes:\n{remote}"
