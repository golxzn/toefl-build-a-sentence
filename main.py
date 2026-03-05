from __future__ import annotations

import sys
from typing import Final
from PySide6.QtWidgets import QApplication

from src.main_menu import MainMenuWindow


APP_NAME: Final[str] = "TOEFL Build a Sentence"


def main() -> None:
    app: QApplication = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    window: MainMenuWindow = MainMenuWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

