
# src/oslolo/cli/commands/list.py
import click
from rich.console import Console
from rich.table import Table
from ...core.archive_manager import ArchiveManager

@click.command(name='list')
@click.argument('archive_path', type=click.Path(exists=True, dir_okay=False))
def list_cmd(archive_path):
    """Lists the contents of an archive."""
    console = Console()
    manager = ArchiveManager()

    table = Table(title=f"Contents of {archive_path}")
    table.add_column("File Path", style="cyan", no_wrap=True)

    try:
        with console.status("[bold green]Reading archive..."):
            contents = manager.list_contents(archive_path)
            for item in contents:
                table.add_row(item)
        
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
