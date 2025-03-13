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

# Third-party imports
from qframelesswindow import FramelessWindow
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

# Local imports
from helpers import icon_path
from configs import globals


class DefaultWindow(FramelessWindow):
    """
    A base helper class for creating frameless windows with a custom title bar and standard configurations.
    """

    def __init__(
        self,
        parent: QWidget,
        window_key: str,
    ):
        """
        Initialize the DefaultWindow.

        Args:
            parent (QWidget): The parent widget.
            handler (Any): The handler window instance.
            window_key (str): The key to access window-specific configurations from globals.
        """
        super().__init__(parent=parent)
        self.wk = window_key

        # Window properties
        self.resize(*globals[self.wk]["def_size"])
        self.setMinimumSize(*globals[self.wk]["minimum_size"])

        # Initialize layout and components
        self.setup_default_layout()

    def start(self, win_bar):
        self.setTitleBar(win_bar)
        self.setWindowTitle(globals[self.wk]["name"])
        self.setWindowIcon(QIcon(f"{icon_path()}/main_icon.ico"))
        self.setObjectName("title_bar")

    def setup_default_layout(self):
        """
        Setup the base window layout. Subclasses should extend this method to add custom widgets.
        """
        # Background widget
        self.win_background = QWidget(self)
        self.win_background.setObjectName("win_default_background")
        self.adjust_background_widget()

        # Main container
        self.widget_container = QWidget(self.win_background)
        self.widget_container.setObjectName("win_default_container")

        # Layout for centering the container
        self.container_layout = QVBoxLayout(self.widget_container)
        self.container_layout.setContentsMargins(8, 8, 8, 8)
        self.container_layout.setSpacing(8)

        # Main layout for the background
        self.layout_main = QVBoxLayout(self.win_background)
        self.layout_main.setContentsMargins(8, globals["win_title"]["height"], 8, 8)
        self.layout_main.addWidget(self.widget_container)

        # Set the layout
        self.setLayout(self.layout_main)

    def adjust_background_widget(self):
        """
        Adjust the background widget size based on the window size.
        """
        window_rect = self.rect()
        window_width = window_rect.width()
        window_height = window_rect.height()
        title_bar_height = globals["win_title"]["height"]
        self.win_background.setGeometry(0, title_bar_height, window_width, window_height - title_bar_height)

    # --- Qt Events ---

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.adjust_background_widget()
