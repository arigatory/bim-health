Этот шаблон используется для разработки ботов Telegram с использованием библиотеки [`aiogram v3.0+`](https://github.com/aiogram/aiogram/tree/dev-3.x).

## SQLAlchemy + Alembic
В коде приведены примеры таблицы User с использованием SQLAlchemy 2.0 и скрипты для Alembic (инициализация Alembic, создание и применение миграций).

Однако, если вы никогда не работали с этими инструментами, обратитесь к документации и узнайте больше о них. Также у меня есть англоязычный [курс по этим инструментам на Udemy](https://www.udemy.com/course/sqlalchemy-alembic-bootcamp/?referralCode=E9099C5B5109EB747126).

![img.png](https://img-c.udemycdn.com/course/240x135/5320614_a8af_2.jpg)

### Для начала использования:
1. Скопируйте `.env.dist` в `.env` и заполните необходимые данные.
2. Создайте новые хендлеры.
3. **Docker:**
   1. Можете сразу запускать проект с Docker, а если у вас его нет, то [скачайте и установите](https://docs.docker.com/get-docker/).
   2. Запустите проект командой `docker-compose up`.
4. **Без Docker:**
   1. Создайте [venv](https://docs.python.org/3/library/venv.html).
   2. Установите зависимости из requirements.txt: `pip install -r requirements.txt --pre`.
   3. Запустите проект командой `python3 bot.py`.

### Как создавать и регистрировать хендлеры:
Создайте модуль `your_name.py` в папке `handlers`.

Создайте роутер в `your_name.py`.
```python
from aiogram import Router
user_router = Router()
```
Можно создавать несколько роутеров в одном модуле и присваивать хендлеры каждому из них. Можно регистрировать хендлеры с помощью декораторов:
```python
@user_router.message(commands=["start"])
async def user_start(message):
    await message.reply("Привет, обычный пользователь!")
```

Перейдите в файл `handlers/__init__.py` и добавьте все роутеры в него:
```python
from .admin import admin_router
from .echo import echo_router
from .user import user_router

...

routers_list = [
    admin_router,
    user_router,
    echo_router,  # echo_router must be last
]

```
### Как добавить хендлеры к нашему боту:
Перейдите к файлу `bot.py` и включите наши роутеры:
```python
from tgbot.handlers import routers_list

...

async def main():
   
    ...

   dp.include_routers(*routers_list)

    ...


```

### Учебники по aiogram v3
Видеоуроков пока нет, но @Groosha уже начал создавать [свой учебник](https://mastergroosha.github.io/aiogram-3-guide).