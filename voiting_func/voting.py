from collections import defaultdict
from typing import List, Dict, Tuple
from utils.expectation import compute_expectation


def apply_expectation_vote(data: List[Dict]) -> Dict[Tuple[int, str, str], Dict]:
    """Применение голосования с вычислением математического ожидания для version_answer."""
    # Группировка данных по module_iteration_num, module_name и experiment_name
    grouped_data = defaultdict(list)
    grouped_versions = defaultdict(set)
    grouped_correct = {}
    for record in data:
        key = (
            record["module_iteration_num"],
            record["module_name"],
            record["experiment_name"],
        )
        grouped_data[key].append(
            (record["version_reliability"], record["version_answer"])
        )
        grouped_versions[key].add(record["version_name"])
        if key not in grouped_correct:
            grouped_correct[key] = record["correct_answer"]

    results = {}
    for key, outputs in grouped_data.items():
        iteration_num, module_name, experiment_name = key

        # Определение ожидаемого количества версий на основе уникальных version_name
        expected_versions = len(grouped_versions[key])
        if not outputs:
            print(
                f"Пропущена группа: итерация {iteration_num}, модуль {module_name}, "
                + "эксперимент {experiment_name} — нет данных"
            )
            continue

        if len(outputs) != len(outputs) // expected_versions * expected_versions:
            print(
                f"Пропущена группа: итерация {iteration_num}, модуль {module_name}, "
                + "эксперимент {experiment_name} — количество версий ({len(outputs)}) "
                + " не соответствует ожидаемому ({expected_versions} уникальных version_name)"
            )
            continue

        voted = compute_expectation(outputs)
        if voted is None:
            print(
                f"Пропущена группа: итерация {iteration_num}, модуль {module_name}, "
                + "эксперимент {experiment_name} — не удалось вычислить математическое ожидание"
            )
            continue

        correct = grouped_correct.get(key)
        # Проверка корректности с использованием epsilon
        epsilon = 0.1
        is_correct = False
        if voted is not None and correct is not None:
            is_correct = abs(voted - correct) <= epsilon

        # Сохранение входных данных для вывода
        probs = [p for p, _ in outputs]
        answers = [a for _, a in outputs]

        results[key] = {
            "voted": voted,
            "correct": correct,
            "is_correct": is_correct,
            "epsilon": epsilon,
            "probs": probs,
            "answers": answers,
        }

    return results
