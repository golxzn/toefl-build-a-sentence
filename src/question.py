from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

def find_line(lines: list[str], key: str) -> str:
    for line in lines:
        if not line.startswith(key): continue

        lines.remove(line)
        return line[len(key):].strip()

    return ''

def safe_to_int(value: str) -> int:
    if len(value) <= 0: return -1

    try:
        return int(value)
    except Exception as e:
        print(f"ERROR: Frozen (F:) Part '{value}' is not a number: {str(e)}")
    return -1


@dataclass(frozen=True)
class Question:
    id: str
    text: str
    answer_parts: List[str]
    trick: List[str]
    frozen: Set[int]

    def is_correct(self, parts: List[str]) -> bool:
        print(f'Comparing "{parts}"\n      and "{self.answer_parts}"')
        return parts == self.answer_parts

    @staticmethod
    def from_file(path: Path) -> "Question":
        id: str = str(path)[str(path).rfind('_') + 1:].removesuffix('.txt')

        lines: List[str] = path.read_text(encoding="utf-8").splitlines()

        q_raw: str = find_line(lines, 'Q:')
        a_raw: str = find_line(lines, 'A:')
        t_raw: str = find_line(lines, 'T:')
        f_raw: str = find_line(lines, 'F:')

        def make_parts(line: str) -> list[str]:
            return list(filter(len, [p.strip().lower() for p in line.split("/")]))

        answer_parts: List[str] = make_parts(a_raw)
        trick_parts: List[str] = make_parts(t_raw)
        frozen_parts: Set[int] = Question.make_frozen_parts(f_raw)

        return Question(id, q_raw, answer_parts, trick_parts, frozen_parts)

    @staticmethod
    def make_frozen_parts(raw: str) -> Set[int]:
        if len(raw) == 0:
            return set()

        frozen_parts: List[int] = [safe_to_int(p.strip()) for p in raw.split("/")]
        if frozen_parts is None:
            return set()

        frozen_parts.sort()
        while len(frozen_parts) > 0 and frozen_parts[0] < 0:
            frozen_parts.pop(0)

        return set(frozen_parts)


