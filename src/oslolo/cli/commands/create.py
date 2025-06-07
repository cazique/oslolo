
# src/oslolo/cli/commands/create.py
import click
from rich.console import Console
from ...core.archive_manager import ArchiveManager
from ...core.format_detector import detect_format

@click.command()
@click.argument('archive_path', type=click.Path())
@click.argument('source_paths', nargs=-1, type=click.Path(exists=True))
def create(archive_path, source_paths):
    """Creates a new archive from specified files and directories."""
    console = Console()
    manager = ArchiveManager()
    
    if not source_paths:
        console.print("[bold red]Error:[/bold red] No source files or directories specified.")
        return

    format_name = detect_format(click.Path().convert(archive_path, None, None))
    if not format_name:
        console.print(f"[bold red]Error:[/bold red] Cannot determine format for '{archive_path}'. Please use a known extension (.zip, .7z, .tar.gz, etc).")
        return

    console.print(f"[*] Creating [cyan]{archive_path}[/] in [yellow]{format_name}[/] format...")
    try:
        manager.create(archive_path, list(source_paths), format=format_name)
        console.print("[bold green]Archive created successfully.[/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
