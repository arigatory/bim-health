from tinydb import TinyDB, Query
from datetime import datetime

# Создание базы данных в файле
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
    # Используйте upsert для замены существующей записи или вставки новой
    db.upsert(data, Query().userId == user_id)


def get_health_status(user_id):
    query = Query().userId == user_id
    result = db.get(query)
    return result


if __name__ == "__main__":
    # Пример использования:
    user_id = 1
    user_name = "Ivan"
    current_date = datetime.now().strftime("%Y-%m-%d")
    health_status = "Healthy"

    save_health_status(user_id, user_name, current_date, health_status)

    retrieved_health_status = get_health_status(user_id)

    if retrieved_health_status:
        print(
            f"Health status for user {user_id} ({user_name}): {retrieved_health_status}")
    else:
        print(f"No health status found for user {user_id}")
