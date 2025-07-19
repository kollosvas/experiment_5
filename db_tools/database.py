import sqlite3
import json
from typing import List, Dict, Optional, Tuple

def connect_to_database(
    input_db_name: str = "experiment_edu.db",
    output_db_name: str = "voting_results.db"
) -> Tuple[Optional[sqlite3.Connection], Optional[sqlite3.Cursor], Optional[sqlite3.Connection], Optional[sqlite3.Cursor]]:
    """Подключение к двум базам данных SQLite: для входных данных и результатов."""
    try:
        # Подключение к базе данных для чтения входных данных
        input_conn = sqlite3.connect(input_db_name)
        input_cursor = input_conn.cursor()
    except sqlite3.Error as e:
        print(f"Ошибка подключения к входной базе данных {input_db_name}: {e}")
        return None, None, None, None

    try:
        # Подключение к базе данных для записи результатов
        output_conn = sqlite3.connect(output_db_name)
        output_cursor = output_conn.cursor()
        # Создание таблицы для результатов голосования, если она не существует
        output_cursor.execute('''
            CREATE TABLE IF NOT EXISTS voting_results (
                module_iteration_num INTEGER,
                module_name TEXT,
                experiment_name TEXT,
                voted REAL,
                correct REAL,
                is_correct INTEGER,
                epsilon REAL,
                probs TEXT,
                answers TEXT,
                PRIMARY KEY (module_iteration_num, module_name, experiment_name)
            )
        ''')
        output_conn.commit()
        return input_conn, input_cursor, output_conn, output_cursor
    except sqlite3.Error as e:
        print(f"Ошибка подключения к выходной базе данных {output_db_name}: {e}")
        input_conn.close()
        return None, None, None, None

def fetch_experiment_data(cursor: sqlite3.Cursor) -> List[Dict]:
    """Извлечение данных из таблицы experiment_data."""
    try:
        cursor.execute('''
            SELECT module_iteration_num, module_name, version_name, version_reliability, 
                   version_answer, correct_answer, experiment_name
            FROM experiment_data
            ORDER BY module_name, module_iteration_num
        ''')
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            data.append({
                "module_iteration_num": row[0],
                "module_name": row[1],
                "version_name": row[2],
                "version_reliability": row[3],
                "version_answer": row[4],
                "correct_answer": row[5],
                "experiment_name": row[6]
            })
                
        return data
    except sqlite3.Error as e:
        print(f"Ошибка при извлечения данных: {e}")
        return []

def save_results_to_database(conn: sqlite3.Connection, cursor: sqlite3.Cursor, results: Dict[Tuple[int, str, str], Dict]):
    """Сохранение результатов голосования в базу данных."""
    try:
        for key, res in results.items():
            iteration_num, module_name, experiment_name = key
            cursor.execute('''
                INSERT OR REPLACE INTO voting_results (
                    module_iteration_num, module_name, experiment_name, 
                    voted, correct, is_correct, epsilon, probs, answers
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                iteration_num, module_name, experiment_name,
                res["voted"], res["correct"], int(res["is_correct"]),
                res["epsilon"], json.dumps(res["probs"]), json.dumps(res["answers"])
            ))
        conn.commit()
        print("Результаты успешно сохранены в базу данных voting_results.db.")
    except sqlite3.Error as e:
        print(f"Ошибка при сохранении результатов: {e}")

        