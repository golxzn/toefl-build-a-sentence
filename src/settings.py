from __future__ import annotations

from pathlib import Path
from typing import Final

from PySide6.QtCore import QSize

ASSETS_DIR: Final[Path] = Path("assets")
TIME_PER_QUESTION: Final[int] = 30
TOTAL_QUESTIONS: Final[int] = 10
TOTAL_TIME: Final[int] = TIME_PER_QUESTION * TOTAL_QUESTIONS

class Settings:
    @staticmethod
    def assetsDir(path: Path = '') -> Path:
        return ASSETS_DIR / path

    @staticmethod
    def timePerQuestion() -> int:
        return TIME_PER_QUESTION

    @staticmethod
    def questionsPerTest() -> int:
        return TOTAL_QUESTIONS

    @staticmethod
    def totalTime() -> int:
        return TOTAL_TIME

    @staticmethod
    def totalTimeFor(questions_count: int) -> int:
        return questions_count * Settings.timePerQuestion()

    @staticmethod
    def maximumSize() -> QSize:
        return QSize(1920, 1080)

    @staticmethod
    def fontSizeStyle() -> str:
        return 'font-size: 22px;'

    @staticmethod
    def oneSecondDurationMs() -> int:
        return 800
