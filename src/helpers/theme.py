# Simple theme helper for global app color handling
# This file is part of NeveBit.

import csv
import logging
from typing import Tuple, Any


class CSVPalette:
    """
    A tiny class that wraps a dict and lets you access
    dict keys as if they were attributes.
    """

    def __init__(self, palette_dict: dict):
        self._data = palette_dict

    def __getattr__(self, name):
        # If the key isn't found, this will raise KeyError
        # which becomes AttributeError, letting you see errors like normal
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f"No attribute or key '{name}' in the palette dictionary")


class ThemeManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
            cls._instance.logger = logging.getLogger("NeveBit")
            cls._instance.themes = {}
            cls._instance.palettes = {}
            cls._instance.current_theme = None
            cls._instance.listeners = []
        return cls._instance

    def load_theme(self, theme_name: str, theme_data, theme_palette):
        if isinstance(theme_palette, dict):
            theme_palette = CSVPalette(theme_palette)
        self.themes[theme_name] = theme_data
        self.palettes[theme_name] = theme_palette

    def set_theme(self, theme_name: str):
        if theme_name in self.themes:
            self.current_theme = theme_name
            for listener in self.listeners:
                try:
                    listener()
                except Exception as e:
                    self.logger.error(f"Error in listener: {e}")
        else:
            raise ValueError(f"Theme '{theme_name}' does not exist")

    def download_theme(self, theme_name: str) -> tuple[dict, object]:
        return self.themes.get(theme_name), self.palettes.get(theme_name)

    def get_current_theme(self) -> Tuple[str, Any, CSVPalette]:
        return self.current_theme, self.themes.get(self.current_theme), self.palettes.get(self.current_theme)

    def sub(self, listener):
        self.listeners.append(listener)

    def unsub(self, listener):
        if listener in self.listeners:
            self.listeners.remove(listener)


class PaletteManager:
    def __init__(self, theme_path):
        self.theme_path = theme_path

    def apply_palette(self, selected_palette_dict: dict, base_qss=None):
        """Applies a selected palette to a QSS template."""

        # Load template from file
        with open(self.theme_path, "r") as file:
            qss_template = file.read()

        # If QSS template is empty, fallback to an empty string
        styled_qss = qss_template if qss_template else (base_qss or "")

        # Loop over dictionary items
        for property_name, color_value in selected_palette_dict.items():
            placeholder = f"{{{{{property_name}}}}}"
            styled_qss = styled_qss.replace(placeholder, color_value)

        return styled_qss

    def apply_geometry(self, selected_geometry, base_qss=None):
        """Applies geometry properties to a QSS template."""
        styled_qss = base_qss or ""
        for attr_name, attr_value in vars(selected_geometry).items():
            if not attr_name.startswith("__"):
                placeholder = f"{{{{{attr_name}}}}}"
                styled_qss = styled_qss.replace(placeholder, str(attr_value))
        return styled_qss

    def parse_palette_csv(self, csv_path: str) -> dict:
        """Reads a CSV file and returns a dictionary of themes and their properties using the csv library."""
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            theme_names = [col.strip() for col in header[1:]]
            themes_data = {theme.lower(): {} for theme in theme_names}

            for row in reader:
                if not row or len(row) < 2:
                    continue

                property_name = row[0].strip()
                for i, theme_name in enumerate(theme_names, start=1):
                    color_value = row[i].strip() if i < len(row) else ""
                    themes_data[theme_name.lower()][property_name] = color_value

        return themes_data
