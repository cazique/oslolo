
# packaging/macos/setup.py
"""
This is a setup.py script for creating a macOS application bundle with py2app.

Usage:
    python setup.py py2app
"""
from setuptools import setup

APP = ['src/oslolo/main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'oslolo.icns',
    'packages': ['PyQt6', 'qtawesome', 'qdarkstyle', 'oslolo'],
    'plist': {
        'CFBundleName': 'OSLolo',
        'CFBundleDisplayName': 'OSLolo',
        'CFBundleGetInfoString': "OSLolo Archive Manager",
        'CFBundleIdentifier': "edu.universidad.oslolo",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': 'Copyright © 2025 Universidad Team. All rights reserved.'
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
