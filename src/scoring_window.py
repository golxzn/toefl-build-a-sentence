from __future__ import annotations

from dataclasses import dataclass
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget

from src.settings import Settings


class ScoringWindow(QWidget):

    @dataclass(frozen=True)
    class Callbacks:
         on_go_back: Callable
         on_save_back: Callable

    def __init__(self, score: int, total: int, wrong: list[str], callbacks: Callbacks) -> None:
        super().__init__()
        self.setWindowTitle("Score")
        self.setMaximumSize(Settings.maximumSize())

        layout: QVBoxLayout = QVBoxLayout(self)

        label: QLabel = QLabel(f"{score} / {total}")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"{Settings.fontSizeStyle()} font-weight: bold;")

        self.go_back: QPushButton = QPushButton("Go Back")
        self.go_back.clicked.connect(callbacks.on_go_back)

        self.save_back: QPushButton = QPushButton("Save & Go Back")
        self.save_back.clicked.connect(callbacks.on_save_back)

        layout.addWidget(self._make_label(f"{score} / {total}", 28))
        layout.addWidget(self.go_back)
        layout.addWidget(self.save_back)

        wrong_list: QListWidget = QListWidget()
        wrong_list.addItems(wrong)

        layout.addWidget(wrong_list)

    def _make_label(self, text: str, font_size: int) -> QLabel:
        label: QLabel = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(f"font-size: {font_size}px; font-weight: bold;")
        return label


