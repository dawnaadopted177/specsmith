# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""Test tools — run pytest and summarize results."""

from __future__ import annotations

import subprocess
import sys
from typing import Annotated


def run_unit_tests(
    test_path: Annotated[
        str, "Test path relative to project root, e.g. 'tests/' or 'tests/test_foo.py'"
    ] = "tests/",
    extra_args: Annotated[str, "Extra pytest arguments, e.g. '-x --tb=short'"] = "--tb=short -q",
    project_dir: str = ".",
) -> str:
    """Run pytest on the project and return the output."""
    cmd = [sys.executable, "-m", "pytest", test_path, *extra_args.split()]
    try:
        result = subprocess.run(  # noqa: S603
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=project_dir,
            timeout=300,
        )
        output = (result.stdout + result.stderr).strip()
        if len(output) > 12000:
            output = output[:12000] + "\n...(truncated)"
        return f"[exit {result.returncode}]\n{output}"
    except subprocess.TimeoutExpired:
        return "[TIMEOUT] pytest exceeded 300s"
    except Exception as e:  # noqa: BLE001
        return f"[ERROR] {e}"


def summarize_failures(test_output: Annotated[str, "Raw pytest output to summarize"]) -> str:
    """Extract and summarize test failures from pytest output."""
    lines = test_output.splitlines()
    failures: list[str] = []
    in_failures = False
    for line in lines:
        if "FAILURES" in line or "FAILED" in line:
            in_failures = True
        if in_failures:
            failures.append(line)
        if "short test summary" in line.lower():
            in_failures = True
    if not failures:
        # Check for pass summary
        for line in lines:
            if "passed" in line.lower():
                return line.strip()
        return "No failure information found in output."
    return "\n".join(failures[-50:])  # last 50 lines of failure info
