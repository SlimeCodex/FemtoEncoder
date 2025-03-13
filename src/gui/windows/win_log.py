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
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPlainTextEdit, QWidget

# Local imports
from gui.widgets.utils.default_window import DefaultWindow
from gui.widgets.utils.title_bar import MinimalWindowBar
from configs import globals


class LogViewerWindow(DefaultWindow):
    def __init__(self, parent: QWidget):

        # Initializes window
        super().__init__(parent=parent, window_key="win_log")
        window_bar = MinimalWindowBar(self)
        super().start(window_bar)
        window_bar.windowClose.connect(self.close_window)

        # Configure and generate the specific layout and widgets
        self.setup_stream_layout()

    def setup_stream_layout(self):
        # Text widget for the data stream viewer
        self.txt_printf = QPlainTextEdit()
        self.txt_printf.setObjectName("printf")
        self.txt_printf.verticalScrollBar().setObjectName("basic")
        self.txt_printf.horizontalScrollBar().setObjectName("basic")
        font = QFont(globals["win_log"]["font"], globals["win_log"]["font_size"])
        self.txt_printf.setFont(font)
        self.txt_printf.setMaximumBlockCount(globals["win_log"]["line_limit"])
        self.txt_printf.setReadOnly(True)

        # Add the text widget to the main layout
        self.container_layout.addWidget(self.txt_printf)
        self.container_layout.setContentsMargins(0, 0, 0, 0)

    def log_data(self, data: str):
        self.txt_printf.insertPlainText(data)

        # Auto-scroll to the bottom
        scrollbar = self.txt_printf.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def close_window(self):
        self.hide()
