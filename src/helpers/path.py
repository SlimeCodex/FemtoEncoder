# Simple path helper for the application
# This file is part of NeveBit.

import sys
import os
from pathlib import Path

def get_base_path():
    """Returns the base path of the application, handling frozen and non-frozen states."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)  # Path when frozen (PyInstaller)
    return Path(__file__).resolve().parent.parent  # Path during development

def icon_path():
    """Returns the path to the icons directory."""
    return get_base_path() / "resources" / "icons"

def font_path():
    """Returns the path to the fonts directory."""
    return get_base_path() / "resources" / "fonts"

def movie_path():
    """Returns the path to the videos directory."""
    return get_base_path() / "resources" / "videos"

def theme_path():
    """Returns the path to the themes directory."""
    return get_base_path() / "configs"

def get_appdata_path(app_name: str, subfolder: str = ""):
    """Returns the default application data folder path based on the operating system."""
    if sys.platform == 'win32':
        base_path = Path(os.getenv('APPDATA')) / app_name
    elif sys.platform == 'darwin':
        base_path = Path.home() / 'Library' / 'Application Support' / app_name
    elif sys.platform == 'linux':
        base_path = Path.home() / f'.{app_name.lower()}'
    else:
        raise RuntimeError("Unsupported operating system")
    return base_path / subfolder if subfolder else base_path
