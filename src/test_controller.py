from __future__ import annotations

import shutil
import random

from pathlib import Path
from typing import List, Final

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget

from src.settings import Settings
from src.question import Question
from src.test_window import TestWindow
from src.scoring_window import ScoringWindow


class TestController:
    def __init__(self, parent: QWidget, mode: str, go_back: Callable) -> None:
        self.parent: QWidget = parent
        self.mode: str = mode
        self.go_back: Callable = go_back
        self.time_left: int = Settings.totalTime()
        self.index: int = 0

        self.questions_paths: List[Path] = self._load_questions()
        self.questions: List[Question] = [Question.from_file(p) for p in self.questions_paths]
        self.answers: List[List[str]] = [None] * len(self.questions)
        self.results: List[bool] = [False] * len(self.questions)

        self.test_window: TestWindow = TestWindow(
            total=len(self.questions),
            on_next=self._show_next
        )
        self.test_window.set_question(
            index=self.index + 1,
            question=self.questions[self.index]
        )

        self.test_window.show()

        self.timer: QTimer = QTimer(self.parent)
        self.timer.timeout.connect(self._tick)
        self.timer.start(Settings.oneSecondTime())

    def _load_questions(self) -> List[Path]:
        questions: list[str] = []
        if self.mode != "random":
            questions = list(Settings.assetsDir(self.mode).glob("*.txt"))
        else:
            questions = list(Settings.assetsDir().rglob("*.txt"))

        random.shuffle(questions)
        return questions[:Settings.questionsPerTest()]

    def _tick(self) -> None:
        self.time_left -= 1
        self.test_window.update_timer(self.time_left)

        if self.time_left <= 0:
            self._finish()

    def _show_next(self) -> None:
        if self.index >= len(self.questions):
            self._finish()
            return

        self.answers[self.index] = self.test_window.current_answer()
        self.index += 1

        if self.index < len(self.questions):
            self.test_window.set_question(
                index=self.index + 1,
                question=self.questions[self.index]
            )

    def _finish(self) -> None:
        self.timer.stop()

        wrong_sentences: list[str] = []
        total: int = len(self.questions)
        for idx in range(total):
            self.results[idx] = self.questions[idx].is_correct(self.answers[idx])
            if not self.results[idx]:
                wrong_sentences.append(' '.join(self.answers[idx]))

        # for i, question in enumerate(self.questions):
        #     self.results[i] = question.is_correct(self.answers[i])

        score: int = sum(self.results)

        self.test_window.hide()
        self.scoring_window: ScoringWindow = ScoringWindow(
            score=score,
            total=total,
            wrong=wrong_sentences,
            callbacks=ScoringWindow.Callbacks(
                on_go_back=lambda: self._exit(False),
                on_save_back=lambda: self._exit(True)
            )
        )

        self.scoring_window.show()

    def reset() -> None:
        self.answers.clear()
        self.questions.clear()
        self.results.clear()
        self.index = 0

    def _exit(self, save: bool) -> None:
        self.test_window.close()
        self.test_window = None

        self.scoring_window.close()
        self.scoring_window = None

        if save:
            for path, correct in zip(self.questions_paths, self.results):
                target: Path = Settings.assetsDir() / ("correct" if correct else "mistaken")
                shutil.move(str(path), target / path.name)
        self.go_back()
