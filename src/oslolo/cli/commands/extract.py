
# src/oslolo/cli/commands/extract.py
import click
from rich.console import Console
from ...core.archive_manager import ArchiveManager

@click.command()
@click.argument('archive_path', type=click.Path(exists=True, dir_okay=False))
@click.option('--dest', '-d', 'dest_path', default='.', type=click.Path(file_okay=False), help="Destination directory.")
def extract(archive_path, dest_path):
    """Extracts files from an archive."""
    console = Console()
    manager = ArchiveManager()
    console.print(f"[*] Extracting [cyan]{archive_path}[/] to [cyan]{dest_path}[/]...")
    try:
        manager.extract(archive_path, dest_path)
        console.print("[bold green]Extraction successful.[/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
