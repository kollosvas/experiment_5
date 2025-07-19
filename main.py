from db_tools.database import connect_to_database, fetch_experiment_data, save_results_to_database
from voiting_func.voting import apply_expectation_vote
from utils.utils import print_results, user_menu

def main():
    # Подключение к двум базам данных
    input_conn, input_cursor, output_conn, output_cursor = connect_to_database()
    if input_conn is None or input_cursor is None or output_conn is None or output_cursor is None:
        return
    
    # Извлечение данных из входной базы
    data = fetch_experiment_data(input_cursor)
    if not data:
        print("Нет данных для обработки.")
        input_conn.close()
        output_conn.close()
        return
    
    # Применение голосования
    results = apply_expectation_vote(data)
    
    # Сохранение результатов в выходную базу
    save_results_to_database(output_conn, output_cursor, results)
    
    # Вывод первых 5 результатов по умолчанию
    print_results(results, num_to_print=5)
    
    # Запуск меню
    user_menu(results)
    
    # Закрытие соединений
    input_conn.close()
    output_conn.close()

if __name__ == "__main__":
    main()