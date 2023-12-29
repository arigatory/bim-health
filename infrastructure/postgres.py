from dataclasses import dataclass
import os
import random
import uuid
import psycopg2
from psycopg2.extras import NamedTupleCursor
from datetime import datetime, timedelta
from dotenv import load_dotenv


load_dotenv()

# Установите параметры подключения к вашей базе данных PostgreSQL
DB_PARAMS = {
    "dbname": os.environ.get('POSTGRES_DB', "bot"),
    "user": os.environ.get('POSTGRES_USER', "ivan"),
    "password": os.environ.get('POSTGRES_PASSWORD', "1qazXSW@"),
    "host": os.environ.get('DB_HOST', "pg_database"),
    "port": os.environ.get('DB_PORT', "5432")
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
        statuses = ["Болен", "Почти выздоровел", "Здоров"]
        for i in range(1, 11):
            for day_offset in range(1, 6):
                id = str(uuid.uuid4())
                date = datetime.now() - timedelta(days=day_offset)
                status = random.choice(statuses)
                item = (id, i, f'Name{i}', status, date)
                data.append(item)

        # Очищаем таблицу в БД, чтобы загружать данные в пустую таблицу
        cursor.execute("""TRUNCATE user_records""")

        args = ','.join(cursor.mogrify("(%s, %s, %s, %s, %s)",
                        item).decode() for item in data)
        cursor.execute(f"""
            INSERT INTO user_records (id, telegramid, name, status, date)
            VALUES {args}
            """)


def insert_data(telegram_id, nickname, status):
    with psycopg2.connect(**DB_PARAMS) as conn, conn.cursor() as cursor:
        id = str(uuid.uuid4())
        date = datetime.now()
        data = (id, telegram_id, nickname, status, date)

        cursor.execute("""INSERT INTO user_records (id, telegramid, name, status, date) 
                       VALUES (%s, %s, %s, %s, %s)""", data)

