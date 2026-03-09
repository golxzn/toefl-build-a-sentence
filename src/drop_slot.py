from __future__ import annotations

from typing import Optional
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QDrag

class DropSlot(QLabel):
    def __init__(self, frozen: bool = False, word: str | None = None) -> None:
        super().__init__(word)
        self.frozen: bool = frozen
        self.tile = None  # type: WordTile | None

        # self.setFixedSize(110, 40)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(40)
        self.setAcceptDrops(True)
        self._update_style()

    # ------------------ visuals ------------------

    def _update_style(self) -> None:
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #999;
                border-radius: 6px;
                background: #fafafa;
                font-size: 22px;
            }
        """)

    # ------------------ drag & drop ------------------

    def dragEnterEvent(self, event) -> None:
        if self.frozen: return

        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event) -> None:
        if not self.frozen and self.set_tile(event.source()):
            event.acceptProposedAction()

    def mousePressEvent(self, event) -> None:
        if self.frozen or event.button() != Qt.LeftButton: return

        mime = QMimeData()
        mime.setText(self.text())

        drag = QDrag(self)
        drag.setMimeData(mime)
        drag.exec(Qt.MoveAction)

    # ------------------ helpers ------------------

    def set_tile(self, tile) -> bool:
        if tile is None:
            return False

        if type(tile) is DropSlot:
            slot = tile
            tile = tile.tile
            slot._release_tile()
        elif tile.current_slot is not None:
            tile.current_slot._release_tile()

        if self.tile is not None:
            self._release_tile()

        self.tile = tile
        tile.current_slot = self
        tile.set_placed(True)

        self.setText(tile.text())
        return True


    def _release_tile(self) -> None:
        if self.tile:
            self.tile.set_placed(False)
            self.tile.current_slot = None

        self.tile = None
        self.setText("")

