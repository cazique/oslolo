
# scripts/build.py
import os
import sys
import platform
import subprocess

def run_command(command):
    print(f"--- Running: {' '.join(command)} ---")
    subprocess.check_call(command)

def build():
    os_name = platform.system()
    
    if os_name == "Windows":
        # Using PyInstaller for Windows
        command = [
            'pyinstaller',
            '--name', 'oslolo',
            '--onefile',
            '--windowed', # Use --console for CLI/TUI debugging
            '--icon', 'packaging/windows/oslolo.ico', # Assumes icon exists
            'src/oslolo/main.py'
        ]
    elif os_name == "Darwin":
        # Using py2app for macOS
        # This requires a setup.py file configured for py2app
        print("macOS build via py2app is not configured in this script.")
        # command = ['python', 'setup_macos.py', 'py2app']
        return
    else: # Linux
        # Using PyInstaller for Linux
        command = [
            'pyinstaller',
            '--name', 'oslolo',
            '--onefile',
            'src/oslolo/main.py'
        ]

    run_command(command)
    print("\n--- Build completed in 'dist' directory ---")

if __name__ == "__main__":
    build()
