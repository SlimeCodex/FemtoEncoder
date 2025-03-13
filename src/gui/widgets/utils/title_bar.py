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
import logging

# Third-party imports
from qframelesswindow import StandardTitleBar
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QLabel, QSpacerItem, QSizePolicy

# Local application/library specific imports
from gui.widgets.utils import SingleButton, ToggleButton
from configs import tooltips, globals
from helpers import icon_path, GlobalEventDispatcher, ThemeManager

# Type hinting for the InterfaceSelectWindow
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.windows.win_main import MainWindow


class MainWindowBar(StandardTitleBar):
    windowClose = pyqtSignal()

    def __init__(
        self,
        handler: 'MainWindow'
    ):
        super().__init__(handler)
        self.titleLabel.setObjectName("title")

        # Instance references
        self.hw = handler

        # Window utils
        self.logger = logging.getLogger('NeveBit')

        # Global dispatcher registration
        self.dispatcher = GlobalEventDispatcher()

        # Global theme manager init
        self.theme_manager = ThemeManager()
        self.theme_manager.sub(self.cb_update_theme)
        self.qss = None

        # Close button reassignment
        #self.closeBtn.clicked.disconnect(self.window().close)
        #self.closeBtn.clicked.connect(lambda: self.close_window())

        # Generate layout
        self.setup_layout()
        self.draw_layout()

    # GUI Functions

    # Set the custom title bar
    def setup_layout(self):

        # Toggle info window button
        self.btn_info = SingleButton(
            icon=(f"{icon_path()}/icon_info.svg"),
            size=globals["gui"]["custom_bar_button_size"],
            callback=(lambda: self.dispatcher.pub("event_toggle_info")),
        )
        self.btn_info.setObjectName("title")
        self.btn_info.setToolTip(tooltips["title_bar"]["info"])

        # Toggle color mode button
        self.btn_theme = SingleButton(
            icon=f"{icon_path()}/icon_palette.svg",
            size=globals["gui"]["custom_bar_button_size"],
            callback=self.toggle_color_mode
        )
        self.btn_theme.setObjectName("title")
        self.btn_theme.setToolTip(tooltips["title_bar"]["theme"])

        # Simple spacer
        hpolicy = QSizePolicy.Policy.Expanding
        vpolicy = QSizePolicy.Policy.Minimum
        self.spc_main = QSpacerItem(10, 20, hpolicy, vpolicy)

    # Inject the custom widgets to the title bar layout
    def draw_layout(self):
        # Program icon position (1)
        # Program name position (2)
        # Main spacer position (3)
        self.layout().insertWidget(4, self.btn_info)
        self.layout().insertWidget(5, self.btn_theme)
        self.layout().insertSpacerItem(6, self.spc_main)
        # Rest of the buttons (min, max, close)

    # Callbacks

    def toggle_color_mode(self):
        self.dispatcher.pub("event_toggle_theme_selector")
        self.logger.debug("Event: event_toggle_theme_selector")

    def cb_toggle_hint(self, status):
        self.dispatcher.pub("event_toggle_hint", status)
        self.logger.debug(f"Event: cb_toggle_hint: {status}")

    # Window Functions

    def cb_update_theme(self):
        name, self.qss, palette = self.theme_manager.get_current_theme()
        self.minBtn.setNormalColor(palette.win_bar_min_button_normal_icon)
        self.minBtn.setHoverColor(palette.win_bar_min_button_hover_icon)
        self.minBtn.setPressedColor(palette.win_bar_min_button_pressed_icon)
        self.maxBtn.setNormalColor(palette.win_bar_max_button_normal_icon)
        self.maxBtn.setHoverColor(palette.win_bar_max_button_hover_icon)
        self.maxBtn.setPressedColor(palette.win_bar_max_button_pressed_icon)
        self.closeBtn.setNormalColor(palette.win_bar_close_button_normal_icon)

        self.btn_info.icon_color(palette.button_svg_icon)
        self.btn_theme.icon_color(palette.button_svg_icon)

    # Qt event

    def close_window(self):
        self.logger.debug("Close window")
        self.windowClose.emit()
        self.close()

    def closeEvent(self, event):
        self.logger.debug("Close event")
        self.windowClose.emit()
        super().closeEvent(event)


# Simplified version of the title bar
class MinimalWindowBar(StandardTitleBar):
    windowClose = pyqtSignal()

    def __init__(self,parent):
        super().__init__(parent)
        self.titleLabel.setObjectName("title")

        # Global theme manager init
        self.theme_manager = ThemeManager()
        self.theme_manager.sub(self.cb_update_theme)

        # Close button reassignment
        self.closeBtn.clicked.disconnect(self.window().close)
        self.closeBtn.clicked.connect(lambda: self.close_window())

    # Window Functions

    def cb_update_theme(self):
        name, qss, palette = self.theme_manager.get_current_theme()
        self.minBtn.setNormalColor(palette.win_bar_min_button_normal_icon)
        self.minBtn.setHoverColor(palette.win_bar_min_button_hover_icon)
        self.minBtn.setPressedColor(palette.win_bar_min_button_pressed_icon)
        self.maxBtn.setNormalColor(palette.win_bar_max_button_normal_icon)
        self.maxBtn.setHoverColor(palette.win_bar_max_button_hover_icon)
        self.maxBtn.setPressedColor(palette.win_bar_max_button_pressed_icon)
        self.closeBtn.setNormalColor(palette.win_bar_close_button_normal_icon)

    def close_window(self):
        self.windowClose.emit()

    # Qt event

    def closeEvent(self, event):
        self.windowClose.emit()
        super().closeEvent(event)


class NotificationWindowBar(StandardTitleBar):
    """Simplified tittle bar for notifications windows"""
    windowClose = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.titleLabel.setObjectName("title")

        # Global theme manager init
        self.theme_manager = ThemeManager()
        self.theme_manager.sub(self.cb_update_theme)

        # Close button reassignment
        self.closeBtn.clicked.disconnect(self.window().close)
        self.closeBtn.clicked.connect(lambda: self.close_window())

        # Disable unused features
        self.setDoubleClickEnabled(False)
        self.minBtn.hide()
        self.maxBtn.hide()

    # Window Functions

    def cb_update_theme(self):
        name, qss, palette = self.theme_manager.get_current_theme()
        self.closeBtn.setNormalColor(palette.win_bar_close_button_normal_icon)

    def close_window(self):
        self.windowClose.emit()

    # Qt event

    def closeEvent(self, event):
        self.windowClose.emit()
        super().closeEvent(event)