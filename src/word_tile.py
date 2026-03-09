from __future__ import annotations

from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QLabel
from src.settings import Settings


class WordTile(QLabel):
    def __init__(self, text: str, tray_index: int) -> None:
        super().__init__(text)
        self.tray_index: int = tray_index
        self.current_slot = None  # type: DropSlot | None

        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(40)
        # tile.setFixedWidth(100)
        self.setStyleSheet(self._normal_style())
        self.setAcceptDrops(False)

    # ------------------ visual states ------------------

    def set_placed(self, placed: bool) -> None:
        self.setStyleSheet(
            self._placed_style() if placed else self._normal_style()
        )

    def _normal_style(self) -> str:
        return f"""
            QLabel {{
                border: 1px solid #666;
                border-radius: 6px;
                padding: 6px 10px;
                background: white;
                {Settings.fontSizeStyle()}
            }}
        """

    def _placed_style(self) -> str:
        return f"""
            QLabel {{
                border: 1px solid #aaa;
                border-radius: 6px;
                padding: 6px 10px;
                background: #ddd;
                color: #666;
                {Settings.fontSizeStyle()}
            }}
        """

    # ------------------ drag logic ------------------

    def mousePressEvent(self, event) -> None:
        if event.button() != Qt.LeftButton:
            return

        drag = QDrag(self)
        mime = QMimeData()
        mime.setText(self.text())
        drag.setMimeData(mime)

        drag.exec(Qt.MoveAction)


