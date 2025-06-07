# src/oslolo/launchers/cli_launcher.py
import click
from ..cli.commands.extract import extract
from ..cli.commands.create import create
from ..cli.commands.list import list_cmd

@click.group()
def cli():
    """OSLolo Command Line Interface."""
    pass

# Agregar comandos al grupo
cli.add_command(extract)
cli.add_command(create)
cli.add_command(list_cmd)

if __name__ == '__main__':
    cli()
