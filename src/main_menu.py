from __future__ import annotations

import os
from pathlib import Path
from typing import Final
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout

from src.settings import Settings
from src.test_controller import TestController


class MainMenuWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("TOEFL – Main Menu")
        self.setMaximumSize(Settings.maximumSize())
        self._build_ui()

    def _build_ui(self) -> None:
        self.buttons_layout: QVBoxLayout = QVBoxLayout()

        self._construct_buttons(self.buttons_layout)

        hbox: QHBoxLayout = QVBoxLayout(self)
        hbox.addStretch(1);
        hbox.addLayout(self.buttons_layout);
        hbox.addStretch(1);

    def _update_buttons(self) -> None:
        self._remove_buttons()
        self._construct_buttons(self.buttons_layout)

    def _construct_buttons(self, layout: QVBoxLayout) -> None:
        unsolved_count: int = len(list(Settings.assetsDir("unsolved").glob("*.txt")))
        mistaken_count: int = len(list(Settings.assetsDir("mistaken").glob("*.txt")))
        correct_count: int = len(list(Settings.assetsDir("correct").glob("*.txt")))
        total_count: int = unsolved_count + mistaken_count + correct_count

        self._add_button(layout, f"Unanswered ({unsolved_count})", "unsolved")
        self._add_button(layout, f"Mistaken ({mistaken_count})", "mistaken")
        self._add_button(layout, f"Answered ({correct_count})", "correct")
        self._add_button(layout, f"Randomly ({total_count})", "random")

    def _remove_buttons(self) -> None:
        targets: list[QWidget] = []
        while self.buttons_layout.count():
            item = self.buttons_layout.takeAt(0)
            widget = item.widget() if item is not None else None
            if widget is not None:
                widget.deleteLater()

    def _add_button(self, layout: QVBoxLayout, text: str, mode: str) -> None:
        button: QPushButton = QPushButton(text)
        button.setStyleSheet(Settings.fontSizeStyle())
        button.clicked.connect(lambda _=False, m=mode: self._start_test(m))
        layout.addWidget(button)

    def _start_test(self, mode: str) -> None:
        self.test_controller: TestController = TestController(
            parent=self,
            mode=mode,
            go_back=self._restore
        )
        self.hide()

    def _restore(self) -> None:
        self._update_buttons()
        self.show()
