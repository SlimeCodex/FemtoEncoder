# Desc: ToggleButton class for toggling between two states
# This file is part of NeveBit.

import logging
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtSvg import QSvgRenderer


class ToggleButton(QPushButton):
    def __init__(
        self,
        parent=None,
        icons=None,
        size=None,
        style=None,
        callback=None,
        toggled=False,
        return_state=True,
    ):
        super().__init__(parent)
        self.logger = logging.getLogger('NeveBit')
        self.icons = icons
        self.toggled = toggled
        self.callback = callback
        self.size = size
        self.rendered_icons = [None, None]
        self.return_state = return_state

        if size is not None:
            self.setFixedSize(*self.size)
        self.setupButton()

        if style:
            self.setStyleSheet(style)

        self.clicked.connect(self.toggleState)

    def setupButton(self):
        icon_id = 1 if self.toggled else 0
        icon = (
            self.rendered_icons[icon_id]
            if self.rendered_icons[icon_id]
            else QIcon(self.icons[icon_id])
        )
        self.setIcon(icon)

    def toggleState(self):
        self.toggled = not self.toggled
        self.setupButton()
        if self.callback:
            if self.return_state:
                self.callback(self.toggled)
            else:
                self.callback()
    
    def get_state(self):
        return self.toggled
    
    def disable(self):
        self.toggled = False
        self.setupButton()
    
    def enable(self):
        self.toggled = True
        self.setupButton()

    def manual_toggle(self):
        self.toggled = not self.toggled
        self.setupButton()

    def renderSvgWithColor(self, icon_id, svg_path, color):
        try:
            svg_renderer = QSvgRenderer(svg_path)
            pixmap = QPixmap(svg_renderer.defaultSize())
            pixmap.fill(QColor(0, 0, 0, 0))

            painter = QPainter(pixmap)
            svg_renderer.render(painter)

            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), QColor(color))

            painter.end()
            self.rendered_icons[icon_id] = QIcon(pixmap)
        except Exception as e:
            self.logger.error(f"Error rendering SVG: {e}")

    def icon_color(self, color):
        self.renderSvgWithColor(0, self.icons[0], color)
        self.renderSvgWithColor(1, self.icons[1], color)
        self.setupButton()


class SingleButton(QPushButton):
    def __init__(self, parent=None, icon=None, size=None, style=None, callback=None):
        super().__init__(parent)
        self.iconPath = icon
        self.callback = callback
        self.renderedIcon = None  # Store the rendered icon

        # Set button icon
        self.updateIcon()

        # Set button size
        if size is not None:
            self.setFixedSize(*size)

        # Apply custom style if provided
        if style:
            self.setStyleSheet(style)

        # Connect the button signal
        self.clicked.connect(self.onButtonPress)

    def updateIcon(self):
        """
        Update the button icon.
        """
        icon = self.renderedIcon if self.renderedIcon else QIcon(self.iconPath)
        self.setIcon(icon)

    def onButtonPress(self):
        """
        Handle the button press event.
        """
        if self.callback:
            self.callback()

    def renderSvgWithColor(self, svg_path, color):
        """
        Render SVG with the specified color.

        :param svg_path: Path to the SVG file.
        :param color: Color in which to render the SVG (e.g., '#ff0000').
        """
        try:
            svg_renderer = QSvgRenderer(svg_path)
            pixmap = QPixmap(svg_renderer.defaultSize())
            pixmap.fill(QColor(0, 0, 0, 0))

            painter = QPainter(pixmap)
            svg_renderer.render(painter)

            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            painter.fillRect(pixmap.rect(), QColor(color))

            painter.end()
            self.renderedIcon = QIcon(pixmap)
            self.updateIcon()
        except Exception as e:
            self.logger.debug(f"Error rendering SVG: {e}")

    def icon_color(self, color):
        """
        Change the icon color.

        :param color: New color in hexadecimal format (e.g., '#ff0000').
        """
        self.renderSvgWithColor(self.iconPath, color)
