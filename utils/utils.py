from typing import Dict, Tuple, Optional

def print_results(results: Dict[Tuple[int, str, str], Dict], num_to_print: Optional[int] = 5):
    """Вывод результатов в консоль, с опцией ограничения количества."""
    # Список для определения порядка модулей
    module_order = ['Module3', 'Module5', 'Module7', 'Module11']
    # Сортировка результатов по module_name в заданном порядке, затем experiment_name, затем module_iteration_num
    items = sorted(results.items(), key=lambda x: (module_order.index(x[0][1]) if x[0][1] in module_order else len(module_order), x[0][2], x[0][0]))
    total = len(items)
    num = total if num_to_print is None else min(num_to_print, total)
    
    for i in range(num):
        key, res = items[i]
        iteration_num, module_name, experiment_name = key
        print(f"\nМодуль: {module_name} Эксперимент: {experiment_name}")
        print(f"Итерация: {iteration_num}")
        print(f"Вероятности: {res['probs']}")
        print(f"Ответы версий: {res['answers']}")
        print(f"Голосование: {res['voted']}")
        print(f"Правильный ответ: {res['correct']}")
        print(f"Верно ли: {res['is_correct']}")
        print(f"Epsilon: {res['epsilon']}")
        print("-" * 50)
    
    print(f"Выведено {num} групп из {total}")

def user_menu(results: Dict[Tuple[int, str, str], Dict]):
    """Интерактивное меню для пользователя."""
    while True:
        print("\nМеню:")
        print("1. Вывести N результатов (укажите число)")
        print("2. Завершить программу")
        choice = input("Выберите опцию (1/2): ").strip()
        
        if choice == '1':
            try:
                n = int(input("Введите количество результатов для вывода: ").strip())
                if n > 0:
                    print_results(results, n)
                else:
                    print("Число должно быть положительным.")
            except ValueError:
                print("Некорректный ввод. Введите число.")
        elif choice == '2':
            print("Программа завершена.")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")