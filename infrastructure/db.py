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


def generate_excel_file(db_path='health_data.json', output_filename='health_data.xlsx'):
    # Создаем пустой DataFrame
    df = pd.DataFrame(columns=['userId', 'userName', 'date', 'status'])

    # Получаем данные из базы TinyDB
    db = TinyDB(db_path)
    data = db.all()

    # Добавляем данные в DataFrame
    for user_data in data:
        user_id = user_data['userId']
        user_name = user_data['userName']
        statuses = user_data.get('statuses', [])

        # Если у пользователя есть статусы, берем последний статус за каждый день
        if statuses:
            latest_statuses = {}
            for status in reversed(statuses):
                date = datetime.strptime(
                    status['date'], "%Y-%m-%d %H:%M:%S.%f").date()
                if date not in latest_statuses:
                    latest_statuses[date] = status
            for date, latest_status in latest_statuses.items():
                df = pd.concat([df, pd.DataFrame({'userId': [user_id], 'userName': [user_name], 'date': [date],
                                                  'status': [latest_status['status']]}),], ignore_index=True)
        else:
            # Если у пользователя нет статусов, пишем "Нет ответа"
            df = pd.concat([df, pd.DataFrame({'userId': [user_id], 'userName': [user_name],
                                              'date': [datetime.now().date()], 'status': ['Нет ответа']}),], ignore_index=True)

    # Переформатируем DataFrame
    df = df.pivot(index=['userId', 'userName'],
                  columns='date', values='status').reset_index()

    # Сортируем столбцы (даты) в порядке возрастания
    df = df.reindex(
        sorted(df.columns[2:], key=lambda x: datetime.strptime(str(x), "%Y-%m-%d")), axis=1)

    # Заполняем пропущенные значения "Нет ответа"
    df = df.fillna('Нет ответа')

    # Сохраняем DataFrame в Excel-файл
    df.to_excel(output_filename, index=False, sheet_name='Sheet1')

    print(f"Excel-файл '{output_filename}' успешно создан.")


# Пример использования
generate_excel_file()
