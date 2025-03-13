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

# Standard imports
import logging

# Third-party imports
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QLabel

# Local imports
from gui.widgets.utils.default_window import DefaultWindow
from gui.widgets.utils.title_bar import NotificationWindowBar


class SupportURLWindow(DefaultWindow):
    def __init__(self, parent: QWidget):

        # Initializes window
        super().__init__(parent=parent, window_key="win_support")
        window_bar = NotificationWindowBar(self)
        super().start(window_bar)
        window_bar.windowClose.connect(self.close_window)

        # Set window properties
        self.setResizeEnabled(False)

        # Window utils
        self.logger = logging.getLogger("NeveBit")

        # Configure and generate the specific layout and widgets
        self.setup_stream_layout()

    def setup_stream_layout(self):
        lbl_support = QLabel(self)
        lbl_support.setText("This will open your web browser to a support page.\nDo you want to continue?")
        lbl_support.setObjectName("basic")
        lbl_support.setWordWrap(True)

        btn_yes = QPushButton("Open Support Page", self)
        btn_yes.setObjectName("basic")
        btn_yes.clicked.connect(self.open_support_page)

        btn_no = QPushButton("Close", self)
        btn_no.setObjectName("basic")
        btn_no.clicked.connect(self.close_window)

        button_layout = QHBoxLayout()
        button_layout.addWidget(btn_yes)
        button_layout.addWidget(btn_no)

        # Main layout
        self.container_layout.addWidget(lbl_support)
        self.container_layout.addLayout(button_layout)

    def open_support_page(self):
        url = QUrl("https://buymeacoffee.com/slimecodex")
        if QDesktopServices.openUrl(url):
            self.logger.info("Support URL opened successfully")
        else:
            self.logger.info("Failed to open support URL")

    def close_window(self):
        self.hide()
