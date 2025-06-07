
# scripts/translate.py
import os
import subprocess
import click

LANGUAGES = ['en', 'es']
DOMAIN = 'messages'
TRANSLATIONS_DIR = 'src/oslolo/translations'
SOURCE_DIR = 'src/oslolo'

@click.group()
def cli():
    """Translation management script for OSLolo."""
    pass

@cli.command()
def update():
    """Extracts messages and updates .po files."""
    click.echo("Updating message catalog...")
    pot_file = f'{TRANSLATIONS_DIR}/{DOMAIN}.pot'
    
    # Using xgettext, a standard tool. Or pybabel extract.
    # This is a simplified example assuming xgettext is on the PATH.
    # A real implementation would use pybabel for better Python support.
    find_cmd = f"find {SOURCE_DIR} -name '*.py' > {TRANSLATIONS_DIR}/sources.txt"
    xgettext_cmd = (
        f"xgettext --from-code=UTF-8 -o {pot_file} "
        f"--keyword=_ --keyword=N_ -f {TRANSLATIONS_DIR}/sources.txt"
    )
    
    click.echo(f"Running: {find_cmd}")
    subprocess.run(find_cmd, shell=True, check=True)
    
    click.echo(f"Running: {xgettext_cmd}")
    subprocess.run(xgettext_cmd, shell=True, check=True)

    for lang in LANGUAGES:
        po_file = f'{TRANSLATIONS_DIR}/{lang}/LC_MESSAGES/{DOMAIN}.po'
        if not os.path.exists(po_file):
             # Create file if it does not exist
            subprocess.run(f"msginit --no-translator -l {lang} -i {pot_file} -o {po_file}", shell=True, check=True)
        else:
            # Merge new strings
            click.echo(f"Updating {po_file}...")
            subprocess.run(f"msgmerge -U {po_file} {pot_file}", shell=True, check=True)
    
    click.echo("Update complete. Now edit the .po files.")

@cli.command()
def compile():
    """Compiles .po files to .mo files."""
    click.echo("Compiling messages...")
    for lang in LANGUAGES:
        po_file = f'{TRANSLATIONS_DIR}/{lang}/LC_MESSAGES/{DOMAIN}.po'
        mo_file = f'{TRANSLATIONS_DIR}/{lang}/LC_MESSAGES/{DOMAIN}.mo'
        cmd = f"msgfmt -o {mo_file} {po_file}"
        click.echo(f"Compiling {lang}: {cmd}")
        subprocess.run(cmd, shell=True, check=True)
    click.echo("Compilation complete.")

if __name__ == '__main__':
    cli()
