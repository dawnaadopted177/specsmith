# SPDX-License-Identifier: MIT
# Copyright (c) 2026 BitConcepts, LLC. All rights reserved.
"""specsmith CLI — Forge governed project scaffolds."""

from __future__ import annotations

from pathlib import Path

import click
import yaml
from rich.console import Console

from specsmith import __version__
from specsmith.config import Platform, ProjectConfig, ProjectType
from specsmith.scaffolder import scaffold_project

console = Console()

PROJECT_TYPE_CHOICES = {
    "1": ProjectType.BACKEND_FRONTEND,
    "2": ProjectType.BACKEND_FRONTEND_TRAY,
    "3": ProjectType.CLI_PYTHON,
    "4": ProjectType.LIBRARY_PYTHON,
    "5": ProjectType.EMBEDDED_HARDWARE,
    "6": ProjectType.FPGA_RTL,
    "7": ProjectType.YOCTO_BSP,
    "8": ProjectType.PCB_HARDWARE,
}

PROJECT_TYPE_LABELS = {
    "1": "Python backend + web frontend",
    "2": "Python backend + web frontend + tray",
    "3": "CLI tool (Python)",
    "4": "Library / SDK (Python)",
    "5": "Embedded / hardware",
    "6": "FPGA / RTL",
    "7": "Yocto / embedded Linux BSP",
    "8": "PCB / hardware design",
}


@click.group()
@click.version_option(version=__version__, prog_name="specsmith")
def main() -> None:
    """specsmith — Forge governed project scaffolds."""


@main.command()
@click.option(
    "--config",
    "config_path",
    type=click.Path(exists=True),
    default=None,
    help="Path to scaffold.yml config file (skips interactive prompts).",
)
@click.option(
    "--output-dir", type=click.Path(), default=".", help="Parent directory for the new project."
)
@click.option("--no-git", is_flag=True, default=False, help="Skip git repository initialization.")
def init(config_path: str | None, output_dir: str, no_git: bool) -> None:
    """Scaffold a new governed project."""
    if config_path:
        raw = _load_config_with_inheritance(config_path)
        cfg = ProjectConfig(**raw)  # type: ignore[arg-type]
        if no_git:
            cfg.git_init = False
    else:
        cfg = _interactive_config(no_git)

    target = Path(output_dir) / cfg.name
    if target.exists() and any(target.iterdir()):
        console.print(f"[red]Error:[/red] Directory {target} already exists and is not empty.")
        raise SystemExit(1)

    console.print(f"\n[bold]Scaffolding [cyan]{cfg.name}[/cyan] ({cfg.type_label})...[/bold]\n")
    created_files = scaffold_project(cfg, target)

    for created in created_files:
        rel = created.relative_to(target)
        console.print(f"  [green]✓[/green] {rel}")

    console.print(
        f"\n[bold green]Done.[/bold green] {len(created_files)} files created in {target}"
    )
    console.print('Open this project in your AI agent and type [bold]"start"[/bold].')

    # Save config as scaffold.yml for re-runs and upgrades
    config_out = target / "scaffold.yml"
    with open(config_out, "w") as fh:
        yaml.dump(cfg.model_dump(mode="json"), fh, default_flow_style=False, sort_keys=False)


def _load_config_with_inheritance(config_path: str) -> dict[str, object]:
    """Load scaffold.yml, merging parent config if `extends` is set."""
    with open(config_path) as f:
        raw: dict[str, object] = yaml.safe_load(f)

    extends = raw.get("extends", "")
    if isinstance(extends, str) and extends and Path(extends).exists():
        with open(extends) as f:
            parent: dict[str, object] = yaml.safe_load(f) or {}
        # Parent provides defaults; child overrides
        merged: dict[str, object] = {
            **parent,
            **{k: v for k, v in raw.items() if k != "extends"},
        }
        return merged

    return raw


VCS_PLATFORM_CHOICES = {"1": "github", "2": "gitlab", "3": "bitbucket", "4": ""}
VCS_PLATFORM_LABELS = {"1": "GitHub", "2": "GitLab", "3": "Bitbucket", "4": "None"}

BRANCH_STRATEGY_CHOICES = {"1": "gitflow", "2": "trunk-based", "3": "github-flow"}
BRANCH_STRATEGY_LABELS = {"1": "Gitflow", "2": "Trunk-based", "3": "GitHub Flow"}

INTEGRATION_OPTIONS = [
    ("agents-md", "AGENTS.md (always included)"),
    ("warp", "Warp / Oz"),
    ("claude-code", "Claude Code"),
    ("copilot", "GitHub Copilot"),
    ("cursor", "Cursor"),
    ("gemini", "Gemini CLI"),
    ("windsurf", "Windsurf"),
    ("aider", "Aider"),
]


def _interactive_config(no_git: bool) -> ProjectConfig:
    """Gather project config interactively."""
    console.print("[bold]specsmith init[/bold] — interactive scaffold setup\n")

    name = click.prompt("Project name")
    console.print("\nProject type:")
    for k, v in PROJECT_TYPE_LABELS.items():
        console.print(f"  {k}. {v}")
    type_choice = click.prompt("Select type", type=click.Choice(list(PROJECT_TYPE_LABELS.keys())))
    project_type = PROJECT_TYPE_CHOICES[type_choice]

    platforms_str = click.prompt(
        "Target platforms (comma-separated)",
        default="windows, linux, macos",
    )
    platforms = [Platform(p.strip().lower()) for p in platforms_str.split(",")]

    language = click.prompt("Primary language", default="python")
    description = click.prompt("Short description", default="")

    # VCS platform
    console.print("\nVCS platform:")
    for k, v in VCS_PLATFORM_LABELS.items():
        console.print(f"  {k}. {v}")
    vcs_choice = click.prompt("Select platform", default="1")
    vcs_platform = VCS_PLATFORM_CHOICES.get(vcs_choice, "github")

    # Branching strategy
    console.print("\nBranching strategy:")
    for k, v in BRANCH_STRATEGY_LABELS.items():
        console.print(f"  {k}. {v}")
    branch_choice = click.prompt("Select strategy", default="1")
    branching_strategy = BRANCH_STRATEGY_CHOICES.get(branch_choice, "gitflow")

    # Agent integrations
    console.print("\nAgent integrations (comma-separated numbers):")
    for i, (_key, label) in enumerate(INTEGRATION_OPTIONS):
        console.print(f"  {i + 1}. {label}")
    int_input = click.prompt("Select integrations", default="1")
    integrations = ["agents-md"]
    for idx_str in int_input.split(","):
        idx = int(idx_str.strip()) - 1
        if 0 <= idx < len(INTEGRATION_OPTIONS):
            name_val = INTEGRATION_OPTIONS[idx][0]
            if name_val not in integrations:
                integrations.append(name_val)

    return ProjectConfig(
        name=name,
        type=project_type,
        platforms=platforms,
        language=language,
        description=description,
        git_init=not no_git,
        vcs_platform=vcs_platform,
        branching_strategy=branching_strategy,
        integrations=integrations,
    )


@main.command()
@click.option("--fix", is_flag=True, default=False, help="Attempt to fix simple issues.")
@click.option(
    "--project-dir",
    type=click.Path(exists=True),
    default=".",
    help="Project root directory.",
)
def audit(fix: bool, project_dir: str) -> None:
    """Run drift and health checks (Section 23 + 26)."""
    from specsmith.auditor import run_audit

    root = Path(project_dir).resolve()
    console.print(f"[bold]Auditing[/bold] {root}\n")
    report = run_audit(root)

    for r in report.results:
        icon = "[green]✓[/green]" if r.passed else "[red]✗[/red]"
        console.print(f"  {icon} {r.message}")

    console.print()
    if report.healthy:
        console.print(f"[bold green]Healthy.[/bold green] {report.passed} checks passed.")
    else:
        console.print(
            f"[bold red]{report.failed} issue(s)[/bold red] found "
            f"({report.fixable} fixable). {report.passed} checks passed."
        )
        if fix:
            from specsmith.auditor import run_auto_fix

            fixed = run_auto_fix(root, report)
            if fixed:
                for msg in fixed:
                    console.print(f"  [cyan]⟳[/cyan] {msg}")
                console.print(
                    f"\n[bold cyan]{len(fixed)} issue(s) auto-fixed.[/bold cyan] "
                    f"Re-run audit to verify."
                )
            else:
                console.print("[yellow]No auto-fixable issues found.[/yellow]")
        raise SystemExit(1)


@main.command()
@click.option(
    "--project-dir",
    type=click.Path(exists=True),
    default=".",
    help="Project root directory.",
)
def validate(project_dir: str) -> None:
    """Check governance file consistency (req ↔ test ↔ arch)."""
    from specsmith.validator import run_validate

    root = Path(project_dir).resolve()
    console.print(f"[bold]Validating[/bold] {root}\n")
    report = run_validate(root)

    for r in report.results:
        icon = "[green]✓[/green]" if r.passed else "[red]✗[/red]"
        console.print(f"  {icon} {r.message}")

    console.print()
    if report.valid:
        console.print(f"[bold green]Valid.[/bold green] {report.passed} checks passed.")
    else:
        console.print(
            f"[bold red]{report.failed} issue(s)[/bold red] found. {report.passed} checks passed."
        )
        raise SystemExit(1)


@main.command()
@click.option(
    "--project-dir",
    type=click.Path(exists=True),
    default=".",
    help="Project root directory.",
)
@click.option(
    "--threshold",
    type=int,
    default=500,
    help="Only compress if ledger exceeds this many lines.",
)
@click.option(
    "--keep-recent",
    type=int,
    default=10,
    help="Number of recent entries to keep.",
)
def compress(project_dir: str, threshold: int, keep_recent: int) -> None:
    """Archive old ledger entries (Section 26.3)."""
    from specsmith.compressor import run_compress

    root = Path(project_dir).resolve()
    result = run_compress(root, threshold=threshold, keep_recent=keep_recent)
    console.print(result.message)


@main.command()
@click.option("--spec-version", default=None, help="Target spec version to upgrade to.")
@click.option(
    "--project-dir",
    type=click.Path(exists=True),
    default=".",
    help="Project root directory.",
)
def upgrade(spec_version: str | None, project_dir: str) -> None:
    """Update governance files to match a newer spec version."""
    from specsmith.upgrader import run_upgrade

    root = Path(project_dir).resolve()
    result = run_upgrade(root, target_version=spec_version)
    console.print(result.message)

    if result.updated_files:
        for f in result.updated_files:
            console.print(f"  [green]✓[/green] {f}")
    if result.skipped_files:
        for f in result.skipped_files:
            console.print(f"  [yellow]—[/yellow] {f} (not found, skipped)")


@main.command()
@click.option(
    "--project-dir",
    type=click.Path(exists=True),
    default=".",
    help="Project root directory.",
)
def status(project_dir: str) -> None:
    """Show VCS platform status (CI, alerts, PRs)."""
    root = Path(project_dir).resolve()
    scaffold_path = root / "scaffold.yml"

    if scaffold_path.exists():
        with open(scaffold_path) as f:
            raw = yaml.safe_load(f)
        platform_name = raw.get("vcs_platform", "github")
    else:
        platform_name = "github"

    if not platform_name:
        console.print("[yellow]No VCS platform configured.[/yellow]")
        return

    from specsmith.vcs import get_platform

    try:
        platform = get_platform(platform_name)
    except ValueError as e:
        console.print(f"[red]{e}[/red]")
        raise SystemExit(1) from e

    if not platform.is_cli_available():
        console.print(
            f"[red]{platform.cli_name} CLI not found.[/red] Install it to use status checks."
        )
        raise SystemExit(1)

    console.print(f"[bold]Status[/bold] via {platform.cli_name}\n")
    ps = platform.check_status()
    for detail in ps.details:
        console.print(f"  {detail}")

    if ps.ci_passing is not None:
        icon = "[green]✓[/green]" if ps.ci_passing else "[red]✗[/red]"
        console.print(f"\n  CI: {icon}")


@main.command()
@click.option(
    "--project-dir",
    type=click.Path(exists=True),
    default=".",
    help="Project root directory.",
)
def diff(project_dir: str) -> None:
    """Compare governance files against spec templates."""
    from specsmith.differ import run_diff

    root = Path(project_dir).resolve()
    results = run_diff(root)

    if not results:
        console.print("[bold green]All governance files match templates.[/bold green]")
        return

    for name, status in results:
        if status == "match":
            console.print(f"  [green]✓[/green] {name}")
        elif status == "missing":
            console.print(f"  [red]✗[/red] {name} — missing")
        else:
            console.print(f"  [yellow]~[/yellow] {name} — differs from template")


if __name__ == "__main__":
    main()
