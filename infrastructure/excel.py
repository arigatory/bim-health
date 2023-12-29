# health_data_manager.py

import pandas as pd
from tinydb import TinyDB, Query
from datetime import datetime

db = TinyDB('health_data.json')


def save_health_status(user_id, user_name, date, status):
    data = {
        "userId": user_id,
        "userName": user_name,
        "statuses": [
            {
                "date": date,
                "status": status
            }
        ]
    }
    db.upsert(data, Query().userId == user_id)


def get_health_status(user_id):
    query = Query().userId == user_id
    result = db.get(query)
    return result


def map_status(status):
    status_mapping = {
        "Healty": "Здоров",
        "Ill": "Болен",
        "Recover": "Выздоравливает"
    }
    return status_mapping.get(status, "Не ответил")


def generate_excel_file(output_filename='health_data.xlsx'):
    users_data = db.all()

    # Строим DataFrame из данных
    df = pd.DataFrame(users_data)

    # Разворачиваем статусы в отдельные столбцы с динамическими названиями дат
    df = pd.concat([df.drop(['statuses'], axis=1),
                   df['statuses'].apply(pd.Series)], axis=1)

    # Сортируем столбцы дат в порядке возрастания
    df = df.sort_values(by=['userId']).sort_index(axis=1)

    # Применяем маппинг статусов
    for column in df.columns[2:]:
        df[column] = df[column].apply(map_status)

    # Заполняем пропущенные значения "Не ответил"
    df = df.fillna('Не ответил')

    # Сохраняем DataFrame в Excel-файл
    df.to_excel(output_filename, index=False, engine='openpyxl')
    print(f"Excel-файл '{output_filename}' успешно создан.")


if __name__ == "__main__":
    # Пример использования:
    user_id = 1
    user_name = "Ivan"
    current_date = datetime.now().strftime("%Y-%m-%d")
    health_status = "Healty"

    save_health_status(user_id, user_name, current_date, health_status)

    # Генерация Excel-файла
    generate_excel_file()
