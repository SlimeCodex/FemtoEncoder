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
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QGroupBox

# Local imports
from gui.widgets.utils.default_window import DefaultWindow
from gui.widgets.utils.title_bar import NotificationWindowBar
from helpers import ThemeManager


class ThemeSelector(DefaultWindow):
    def __init__(self, parent: QWidget):
        # Initializes window
        super().__init__(parent=parent, window_key="win_theme")
        window_bar = NotificationWindowBar(self)
        super().start(window_bar)
        window_bar.windowClose.connect(self.close_window)

        # Global theme manager init
        self.theme_manager = ThemeManager()

        # Configure and generate the specific layout and widgets
        self.setup_stream_layout()

    def setup_stream_layout(self):
        themes = {
            "Dark": ["carbon", "night", "forest", "slate", "mahogany", "carbon_deut", "night_prot", "forest_trit"],
            "Light": ["neve", "book", "ice", "cloud", "sand", "neve_deut", "book_prot", "ice_trit"],
        }
        main_layout = QHBoxLayout()

        for theme_type, theme_names in themes.items():
            group_box = QGroupBox(theme_type)
            group_box.setObjectName("basic")
            vbox = QVBoxLayout()
            for theme_name in theme_names:
                btn = QPushButton(theme_name.replace("_", " ").title())
                btn.setObjectName("basic")
                btn.clicked.connect(lambda checked, name=theme_name: self.theme_manager.set_theme(name))
                vbox.addWidget(btn)
            group_box.setLayout(vbox)
            main_layout.addWidget(group_box)

        btn_close = QPushButton("Close")
        btn_close.setObjectName("basic")
        btn_close.clicked.connect(self.close_window)

        overall_layout = QVBoxLayout()
        overall_layout.addLayout(main_layout)
        overall_layout.addWidget(btn_close)

        self.container_layout.addLayout(overall_layout)

    def close_window(self):
        self.hide()
