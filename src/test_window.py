from __future__ import annotations

import time
import random
from typing import List, Callable

from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

from src.settings import Settings
from src.question import Question
from src.word_tile import WordTile
from src.drop_slot import DropSlot


class TestWindow(QWidget):
    def __init__(self, total: int, on_next: Callable[[], None], on_back: Callable[[], None]) -> None:
        super().__init__()
        self.on_next: Callable[[], None] = on_next
        self.on_back: Callable[[], None] = on_back
        self.slots: List[DropSlot] = []
        self.total: int = total

        self.setWindowTitle("Build a Sentence")
        self.setMaximumSize(Settings.maximumSize())
        self._build_ui()

    def set_question(self, index: int, question: Question, answer: List[str]) -> None:
        self.test_id.setText(f'#{question.id}')
        self.counter.setText(f"{index} / {self.total}")
        self.next_btn.setText("Finish" if index == self.total else "Next")

        self._clear_layout(self.slots_layout)
        self._clear_layout(self.tray_layout)

        self.slots.clear()

        self.question_label.setText(f"<b>Q:</b> {question.text}")
        self.question_label.setStyleSheet(Settings.fontSizeStyle());

        # Building tiles
        answer_parts: list[str] = question.answer_parts.copy()
        for id in reversed(sorted(list(question.frozen))):
            answer_parts.pop(id)

        words: list[str] = answer_parts + question.trick
        random.shuffle(words)

        answered_tiles: List[WordTile] = [None] * len(question.answer_parts)
        self.tray_layout: QHBoxLayout = QHBoxLayout()
        for i, word in enumerate(words):
            tile: WordTile = WordTile(word, i)
            tile.adjustSize()
            self.tray_layout.addWidget(tile)

            if answer is None: continue

            for j, part in enumerate(answer):
                if part != word: continue
                answered_tiles[j] = tile
                break


        # Building slots
        self.slots_layout: QHBoxLayout = QHBoxLayout()
        for i, part in enumerate(question.answer_parts):
            is_frozen: bool = i in question.frozen
            slot: DropSlot = DropSlot(
                frozen=is_frozen,
                word=part if is_frozen else None
            )
            if not is_frozen and answered_tiles[i] is not None:
                slot.set_tile(answered_tiles[i])

            self.slots.append(slot)
            self.slots_layout.addWidget(slot)

        # Packing
        self.layout.insertLayout(2, self.slots_layout, 1)
        self.layout.insertLayout(3, self.tray_layout, 1)

    def update_timer(self, seconds: int) -> None:
        self.timer_label.setText(time.strftime('%M:%S', time.gmtime(seconds)))

    def parse_answer(self) -> list[str]:
        return [slot.text() or "" for slot in self.slots]

    def _build_ui(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)

        header: QHBoxLayout = QHBoxLayout()
        self.counter: QLabel = QLabel()
        self.timer_label: QLabel = QLabel("")
        header.addWidget(self.counter)
        header.addStretch()
        header.addWidget(self.timer_label)
        self.layout.addLayout(header)

        self.question_label: QLabel = QLabel()
        self.layout.addWidget(self.question_label, 1)

        self.slots_layout: QHBoxLayout = QHBoxLayout()
        self.layout.addLayout(self.slots_layout, 1)

        self.tray_layout: QHBoxLayout = QHBoxLayout()
        self.layout.addLayout(self.tray_layout, 1)

        self.back_btn: QPushButton = QPushButton("Back")
        self.back_btn.setStyleSheet(Settings.fontSizeStyle())
        self.back_btn.clicked.connect(self.on_back)

        self.test_id: QLabel = QLabel()

        self.next_btn: QPushButton = QPushButton("Next")
        self.next_btn.setStyleSheet(Settings.fontSizeStyle())
        self.next_btn.clicked.connect(self.on_next)

        footer: QHBoxLayout = QHBoxLayout()
        footer.addWidget(self.back_btn)
        footer.addStretch()
        footer.addWidget(self.test_id)
        footer.addStretch()
        footer.addWidget(self.next_btn)
        self.layout.addLayout(footer)

    def _clear_layout(self, layout: QLayout) -> None:
        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                continue

            widget = item.widget()
            if widget is not None:
                # widget.setParent(None)
                widget.deleteLater()
                continue

            child_layout = item.layout()
            if child_layout is not None:
                self._clear_layout(child_layout)

