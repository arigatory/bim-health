from tinydb import TinyDB, Query
from datetime import datetime
import pandas as pd
from openpyxl import Workbook
# from openpyxl.styles import Alignment

# Создание базы данных в файле
db = TinyDB('health_data.json')


def save_health_status(user_id, status):
    stored = get_health_status(user_id)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    if stored:
        stored['statuses'].append({
            "date": current_date,
            "status": status
        })
        db.upsert(stored, Query().userId == user_id)

    else:
        data = {
            "userId": user_id,
            "userName": 'user_name',
            "statuses": [
                {
                    "date": current_date,
                    "status": status
                }
            ]
        }
        db.upsert(data, Query().userId == user_id)
    # Используйте upsert для замены существующей записи или вставки новой


def get_health_status(user_id):
    query = Query().userId == user_id
    result = db.get(query)
    return result


if __name__ == "__main__":
    # Пример использования:
    user_id = 1
    user_name = "Ivan"
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    health_status = "Healthy"

    save_health_status(user_id, user_name, current_date, health_status)

    retrieved_health_status = get_health_status(user_id)

    if retrieved_health_status:
        print(
            f"Health status for user {user_id} ({user_name}): {retrieved_health_status}")
    else:
        print(f"No health status found for user {user_id}")
