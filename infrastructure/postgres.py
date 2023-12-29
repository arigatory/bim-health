from dataclasses import dataclass
import random
import uuid
import psycopg2
from psycopg2.extras import NamedTupleCursor
from datetime import datetime, timedelta


# Установите параметры подключения к вашей базе данных PostgreSQL
DB_PARAMS = {
    "dbname": "bot",
    "user": "ivan",
    "password": "1qazXSW@",
    "host": "localhost",
    "port": "5439"
}


@dataclass
class UserRecord:
    id: uuid.UUID
    telegramId: int
    name: str
    status: str
    date: datetime


def fetch_users_from_database():
    users = []

    # Подключение к базе данных PostgreSQL
    with psycopg2.connect(**DB_PARAMS, cursor_factory=NamedTupleCursor) as connection:
        with connection.cursor() as cursor:
            # Выполнение SQL-запроса для выборки данных из таблицы
            cursor.execute("SELECT * FROM user_records")
            rows = cursor.fetchall()

            # Преобразование данных в объекты UserRecord и добавление их в список
            for row in rows:
                user = UserRecord(*row)
                users.append(user)

    return users


def get_user_record_by_date(telegram_id, date):
    with psycopg2.connect(**DB_PARAMS, cursor_factory=NamedTupleCursor) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM user_records
                WHERE telegramId = %s AND created::date = %s
            """, (telegram_id, date.date()))
            row = cursor.fetchone()
            if row:
                return UserRecord(*row)
            else:
                return None


def insert_test_data():
    with psycopg2.connect(**DB_PARAMS) as conn, conn.cursor() as cursor:
        data = []
        statuses = ["Болен", "Выздоравливает", "Здоров"]
        for i in range(1, 11):
            for day_offset in range(1, 6):
                id = str(uuid.uuid4())
                date = datetime.now() - timedelta(days=day_offset)
                status = random.choice(statuses)
                item = (id, i, f'Name{i}', status, date)
                data.append(item)

        # Очищаем таблицу в БД, чтобы загружать данные в пустую таблицу
        cursor.execute("""TRUNCATE user_records""")

        # data = [('127551d6-2f7f-4b6b-bdb3-da19c98e1516',
        #         '11', 'Ivan', random.choice(statuses), datetime.now()),
        #         ('f80fdf12-0ff3-4875-9483-5f8d2593446a',
        #         '12', 'Ivan', random.choice(statuses), datetime.now()),
        #         ('002e18a2-b469-4ecc-836b-b18f9ce8df0d',
        #         '13', 'Ivan', random.choice(statuses), datetime.now()),
        #         ('af36613b-be73-4e85-8055-125e906a2a93',
        #         '14', 'Ivan', random.choice(statuses), datetime.now())]
        args = ','.join(cursor.mogrify("(%s, %s, %s, %s, %s)",
                        item).decode() for item in data)
        cursor.execute(f"""            
            INSERT INTO user_records (id, telegramid, name, status, date)
            VALUES {args}
            """)


insert_test_data()