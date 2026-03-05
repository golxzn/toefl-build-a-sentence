from __future__ import annotations

import sys
from pathlib import Path
from typing import List


OUTPUT_PREFIX: str = "assets/unsolved/question_"

def parse(raw: str) -> List[str]:
    parts: List[str] = raw.split("```")
    blocks: List[str] = []

    for part in parts:
        text: str = part.strip()
        if not text:
            continue
        blocks.append(text.removeprefix("txt").strip())

    return blocks

def main() -> None:
    file_names: list[Path] = list(Path('assets/').glob('**/*.txt'))
    ids: list[int] = []
    for name in file_names:
        strname = str(name)
        id: str = strname[strname.find('_') + 1: strname.find('.txt')]
        ids.append(int(id))

    offset: int = sorted(ids)[-1]

    print(f'Reading "{sys.argv[1]}"')
    raw: str = Path(sys.argv[1]).read_text(encoding="utf-8")

    blocks: List[str] = parse(raw)

    print(f"Blocks count: {len(blocks)}")
    for index, content in enumerate(blocks):
        out_path: Path = Path(f"{OUTPUT_PREFIX}{offset + index}.txt")
        print(f'Producing "{str(out_path)}"')
        out_path.write_text(content + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

