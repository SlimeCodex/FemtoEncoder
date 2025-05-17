from PyQt6.QtCore import QPropertyAnimation, pyqtSlot, QEasingCurve
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QToolButton, QSizePolicy
from PyQt6.QtCore import Qt

class CollapsibleBox(QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)

        self.toggle_button = QToolButton(text=title, checkable=True, checked=True)
        self.toggle_button.setStyleSheet("QToolButton {border: none;} QToolButton::checked {font-weight: bold;}")
        self.toggle_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(Qt.ArrowType.DownArrow)
        self.toggle_button.clicked.connect(self.on_toggle)

        self.content_area = QWidget(maximumHeight=0)
        self.content_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.toggle_animation = QPropertyAnimation(self.content_area, b"maximumHeight")
        self.toggle_animation.setDuration(250)
        self.toggle_animation.setEasingCurve(QEasingCurve.Type.InOutQuart)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.content_area)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.content_area.setMaximumHeight(16777215)

    def setContentLayout(self, content_layout):
        self.content_area.setLayout(content_layout)
        collapsed_height = 0
        content_height = content_layout.sizeHint().height()
        self.content_area.setMaximumHeight(content_height)
        self.toggle_animation.setStartValue(collapsed_height)
        self.toggle_animation.setEndValue(content_height)

    @pyqtSlot(bool)
    def on_toggle(self, checked):
        self.toggle_button.setArrowType(Qt.ArrowType.DownArrow if checked else Qt.ArrowType.RightArrow)
        self.toggle_animation.setDirection(
            QPropertyAnimation.Direction.Forward if checked else QPropertyAnimation.Direction.Backward
        )
        self.toggle_animation.start()
