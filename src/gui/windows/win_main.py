#
# This file is part of NeveBit.
# Copyright (C) 2024 SlimeCodex
#
# NeveBit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NeveBit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NeveBit. If not, see <https://www.gnu.org/licenses/>.
#

# Standard library imports
import traceback
import sys

# Third-party imports
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFontDatabase, QFont
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QPushButton, QLineEdit, QWidget

# Local import
from gui.widgets.utils.default_window import DefaultWindow
from gui.widgets.utils.title_bar import MainWindowBar
from gui.windows.win_log import LogViewerWindow
from gui.windows.win_support import SupportURLWindow
from gui.windows.win_theme import ThemeSelector
from gui.widgets.views import FirmwareEncoder
from gui.widgets.utils import SingleButton
from helpers import (
    GlobalEventDispatcher,
    icon_path,
    font_path,
    theme_path,
    setup_logging,
    PaletteManager,
    ThemeManager,
)
from configs import (
    globals,
    tooltips,
    app_geometry,
)


class MainWindow(DefaultWindow):
    """Main application window for NeveBit."""

    def __init__(self, app_main=None, parent=None, arguments=None):
        self.app_main = app_main

        # Initializes window
        super().__init__(parent=parent, window_key="win_app")
        window_bar = MainWindowBar(self)
        super().start(window_bar)

        # Dispatcher initialization
        self.dispatcher = GlobalEventDispatcher()
        self.dispatcher.pub("frameless_instance", self)
        self.dispatcher.sub("event_toggle_info", self.cb_toggle_info)
        self.dispatcher.pub("event_toggle_adder", False)
        self.dispatcher.pub("event_toggle_hint", False)
        self.dispatcher.pub("auto_autosync", True)

        # Register global events
        self.dispatcher.sub("event_toggle_hint", self.cb_toggle_hint)
        self.dispatcher.sub("event_central_close", self.cb_central_close)
        self.dispatcher.sub("event_toggle_theme_selector", self.toggle_theme_selector_window)

        # Global theme manager init
        self.theme_manager = ThemeManager()
        self.theme_manager.sub(self.cb_update_theme)

        # Error window initialization
        self.log_window = LogViewerWindow(None)
        self.log_window.hide()

        # Raw Traffic window initialization
        self.support_url_window = SupportURLWindow(None)
        self.support_url_window.hide()

        # Raw Traffic window initialization
        self.theme_selector_window = ThemeSelector(None)
        self.theme_selector_window.hide()

        # Setup the logger
        self.logger, self.qt_handler = setup_logging()
        self.qt_handler.log_signal.connect(self.display_log_message)

        # Load the font file (.ttf or .otf)
        ubuntu_path = f"{font_path()}/Ubuntu-Regular.ttf"
        QFontDatabase.addApplicationFont(ubuntu_path)
        inconsolata_path = f"{font_path()}/Inconsolata-Regular.ttf"
        QFontDatabase.addApplicationFont(inconsolata_path)
        self.app_main.setFont(QFont("Ubuntu"))

        # Draw the layout
        self.setup_layout()
        self.draw_layout()

        # Check for tactile mode in arguments
        self.tactile_mode = self.parse_tactile_argument(arguments)

        # Enable tactile mode if necessary
        if self.tactile_mode:
            self.enable_tactile_mode()

        # Compile program theme and geometries
        self.compile_themes()

        # Set the custom title and status bar
        self.dispatcher.pub("event_link_status", "offline")

    # --- GUI Functions ---

    def setup_layout(self):
        # Container for the Interface Select Window
        self.interface_container = FirmwareEncoder(self)

        """Setup the layout for the main window."""
        # Single line text area for displaying debug info
        self.line_edit_debug = QLineEdit()
        self.line_edit_debug.setObjectName("debug_bar")
        self.line_edit_debug.setReadOnly(True)
        self.line_edit_debug.setVisible(False)

        # Single line text area for displaying version
        self.line_edit_version = QPushButton()
        self.line_edit_version.setObjectName("basic")
        self.line_edit_version.setFixedWidth(80)
        self.line_edit_version.setVisible(False)
        self.line_edit_version.setText(globals["win_app"]["version"])

        self.btn_log_viewer = SingleButton(
            icon=f"{icon_path()}/icon_terminal.svg",
            size=globals["gui"]["def_button_size"],
            callback=self.toggle_log_window,
        )
        self.btn_log_viewer.setObjectName("basic")
        self.btn_log_viewer.setToolTip(tooltips["main_window"]["log_viewer"])
        self.btn_log_viewer.setVisible(False)

        self.btn_support = SingleButton(
            icon=f"{icon_path()}/icon_coffee.svg",
            size=globals["gui"]["def_button_size"],
            callback=self.toggle_support_window,
        )
        self.btn_support.setIconSize(QSize(32, 32))
        self.btn_support.setObjectName("basic")
        self.btn_support.setToolTip(tooltips["main_window"]["support"])
        self.btn_support.setVisible(False)

    def draw_layout(self):
        """Draw the layout for the main window."""
        debug_layout = QHBoxLayout()
        debug_layout.addWidget(self.btn_log_viewer)
        debug_layout.addWidget(self.line_edit_debug)
        debug_layout.addWidget(self.line_edit_version)
        debug_layout.addWidget(self.btn_support)

        # Main layout
        self.container_layout.addWidget(self.interface_container)
        self.container_layout.addLayout(debug_layout)

    # Window Functions

    def display_log_message(self, formatted_message, unformatted_message, level_name):
        """Display a log message in the debug bar."""
        self.log_window.log_data(formatted_message)

        if level_name == "INFO":  # Only info level logs are showed
            self.line_edit_debug.setText(f"> {unformatted_message}")

    def parse_tactile_argument(self, arguments):
        """Parse the command line arguments for tactile mode."""
        if arguments:
            return "--tactile" in arguments
        return "--tactile" in sys.argv

    def enable_tactile_mode(self):
        """Enables tactile mode for touch input."""
        self.logger.debug("Tactile mode enabled: hiding cursor and adjusting for touch input.")
        self.app_main.setOverrideCursor(Qt.CursorShape.BlankCursor)
        self.showFullScreen()

    # --- Callbacks ---

    def compile_themes(self):
        """Compile the themes for the application."""
        palette_helper = PaletteManager(f"{theme_path()}/app_template.qss")
        dark_palette = palette_helper.parse_palette_csv(f"{theme_path()}/dark_palette.csv")
        light_palette = palette_helper.parse_palette_csv(f"{theme_path()}/light_palette.csv")

        # Generate app color and geometry
        palette = {**dark_palette, **light_palette}
        geometry = app_geometry()

        # Load themes
        for theme_name, theme_properties in palette.items():
            qss = palette_helper.apply_palette(theme_properties, base_qss=None)
            qss = palette_helper.apply_geometry(geometry, qss)
            self.theme_manager.load_theme(theme_name, qss, theme_properties)

        # Load default theme
        self.theme_manager.set_theme(globals["gui"]["theme"])
        self.cb_update_theme()  # Required to apply the initial theme

    # Apply the selected theme
    def cb_update_theme(self):
        """Update the theme for the application."""
        name, qss, palette = self.theme_manager.get_current_theme()
        QApplication.instance().setStyleSheet(qss)
        self.btn_log_viewer.icon_color(palette.button_svg_icon)
        self.btn_support.icon_color(palette.button_svg_icon)

    def cb_toggle_info(self):
        """Toggle the visibility of the debug bar."""
        self.btn_log_viewer.setVisible(not self.btn_log_viewer.isVisible())
        self.line_edit_debug.setVisible(not self.line_edit_debug.isVisible())
        self.line_edit_version.setVisible(not self.line_edit_version.isVisible())
        self.btn_support.setVisible(not self.btn_support.isVisible())

    def toggle_log_window(self):
        """Toggle the visibility of the log window."""
        self.log_window.setVisible(not self.log_window.isVisible())

    def toggle_stream_viewer_window(self):
        """Toggle the visibility of the stream viewer window."""
        self.stream_window.setVisible(not self.stream_window.isVisible())

    def toggle_support_window(self):
        """Toggle the visibility of the support URL window."""
        self.support_url_window.setVisible(not self.support_url_window.isVisible())

    def toggle_theme_selector_window(self):
        """Toggle the visibility of the theme selector window."""
        self.theme_selector_window.setVisible(not self.theme_selector_window.isVisible())

    def cb_toggle_hint(self, status):
        """Callback for toggling the always on top feature."""
        if status:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
            self.updateFrameless()
        else:
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, False)
            self.updateFrameless()
        self.show()

    # --- Qt Events ---

    def cb_central_close(self):
        """Application bar callback to close the application."""
        self.close()

    def closeEvent(self, event):
        """Close the application."""
        self.logger.debug("Closing application...")
        if self.qt_handler:
            self.logger.removeHandler(self.qt_handler)
            self.qt_handler.close()
            self.qt_handler = None
        event.accept()

    # --- Exception Handling ---

    def exception_hook(self, exctype, value, tb):
        formatted_traceback = "".join(traceback.format_exception(exctype, value, tb))
        self.logger.debug(formatted_traceback)
        self.log_window.log_data(formatted_traceback)
        self.log_window.show()
