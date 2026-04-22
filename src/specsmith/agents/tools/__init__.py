# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""AG2 tool functions — filesystem, shell, git, tests, docs.

All tools are plain functions with type annotations that AG2 can register
as callable tools. They use pathlib for filesystem ops (no subprocess)
and structured returns for shell/git ops.
"""

from specsmith.agents.tools.filesystem import (
    list_tree,
    patch_file,
    read_file,
    search_content,
    write_file,
)
from specsmith.agents.tools.git import git_branch_info, git_changed_files, git_diff, git_status
from specsmith.agents.tools.shell import run_project_command
from specsmith.agents.tools.tests import run_unit_tests, summarize_failures

__all__ = [
    "list_tree",
    "patch_file",
    "read_file",
    "search_content",
    "write_file",
    "git_branch_info",
    "git_changed_files",
    "git_diff",
    "git_status",
    "run_project_command",
    "run_unit_tests",
    "summarize_failures",
]
