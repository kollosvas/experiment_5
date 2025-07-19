from typing import List, Tuple, Optional


def compute_expectation(outputs: List[Tuple[float, float]]) -> Optional[float]:
    """
    Вычисляет математическое ожидание значений version_answer с весами version_reliability.
    """
    if not outputs:
        return None

    probs = [p for p, _ in outputs]
    answers = [a for _, a in outputs]

    # Проверка, что все вероятности и ответы — числа
    if not all(isinstance(p, (int, float)) for p in probs) or not all(
        isinstance(a, (int, float)) for a in answers
    ):
        return None

    # Нормализация вероятностей
    prob_sum = sum(probs)
    if abs(prob_sum) < 1e-10:  # Проверка на нулевую сумму
        return None
    normalized_probs = [p / prob_sum for p in probs] if prob_sum != 1 else probs

    # Вычисление математического ожидания
    expected_value = sum(p * a for p, a in zip(normalized_probs, answers))
    return round(expected_value, 6)  # Округление для читаемости
