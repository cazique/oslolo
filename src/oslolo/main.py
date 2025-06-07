# src/oslolo/main.py
import sys
import argparse
from .utils.logger import setup_logging

def entry_point():
    """Main entry point for the OSLolo application."""
    setup_logging()

    # Parsing simple para detectar modo
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--tui', 'tui']:
            # TUI Mode
            try:
                from .launchers import tui_launcher
                tui_launcher.run_tui()
            except ImportError as e:
                print(f"Error loading TUI: {e}")
                sys.exit(1)
        elif sys.argv[1] in ['extract', 'create', 'list']:
            # CLI Mode  
            try:
                from .launchers import cli_launcher
                cli_launcher.cli()
            except ImportError as e:
                print(f"Error loading CLI: {e}")
                sys.exit(1)
        else:
            # GUI Mode (default) o archivo a abrir
            try:
                from .launchers import gui_launcher
                archive_to_open = sys.argv[1] if not sys.argv[1].startswith('--') else None
                gui_launcher.run_gui(archive_path=archive_to_open)
            except ImportError as e:
                print(f"Error loading GUI: {e}")
                sys.exit(1)
    else:
        # Default to GUI
        try:
            from .launchers import gui_launcher
            gui_launcher.run_gui()
        except ImportError as e:
            print(f"Error loading GUI: {e}")
            sys.exit(1)

if __name__ == '__main__':
    entry_point()
