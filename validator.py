from pathlib import Path

from src.settings import Settings
from src.question import Question


ASSETS_DIR: Path = Path("assets/")
SIMILARITY_THRESHOLD: float = 0.25


def find_questions(root_dir: Path, ext: str = '.txt') -> tuple[Path, Question]:
    for path in root_dir.rglob(f"*{ext}"):
        if path.is_file():
            yield path, Question.from_file(path)


def is_invalid(question: Question) -> bool:
    parts_count: int = len(question.answer_parts)
    if parts_count == 0:
        return False;

    if not any(id >= parts_count for id in question.frozen):
        return False

    return True


def get_similarity(question: Question) -> bool:
    def normalize(text: str) -> list[str]:
        return list(filter(len, text.strip().strip('.,!?').lower().split(' ')))

    def calc_similarity(lhv: list[str], rhv: list[str]) -> float:
        ls = set(lhv)
        rs = set(rhv)
        return len(ls & rs) / len(ls | rs)

    prompt: list[str] = normalize(question.text)
    answer: list[str] = normalize(' '.join(question.answer_parts))
    return calc_similarity(prompt, answer)


def relocate(path: Path, subdir_name: str) -> Path:
    target_dir = path.parent.parent / subdir_name
    target_dir.mkdir(parents=True, exist_ok=True)

    target = target_dir / path.name
    return path.rename(target)

def main() -> None:
    broken: list[tuple[Path, Question]] = []
    similar_records: list[tuple[Path, Question]] = []
    similarities: list[tuple[float, int]] = []
    for path_question in find_questions(ASSETS_DIR):
        question: Question = path_question[1]
        if is_invalid(question):
            broken.append(path_question)
            continue

        similarity: float = get_similarity(question)
        if similarity <= SIMILARITY_THRESHOLD:
            continue

        similarities.append((similarity, len(similar_records)))
        similar_records.append(path_question)

    similarities.sort(key=lambda x: x[0])
    for similarity, idx in similarities:
        path, question = similar_records[idx]
        print(f'#{question.id} ({similarity}) {path}:')
        print(' Q:', question.text)
        print(' A:', ' '.join(question.answer_parts).replace(' ,', ','))

    print("BROKEN :", len(broken))
    print("SIMILAR:", len(similarities))

    # for path, _ in broken:
        # relocate(path, 'broken')
        #
    # for path, _ in similar_records:
    #     relocate(path, 'similar')

if __name__ == '__main__':
    main()
