import asyncio
import logging

import betterlogging as bl
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder

from tgbot.config import load_config, Config
from tgbot.handlers import routers_list
from tgbot.middlewares.config import ConfigMiddleware
from tgbot.services import broadcaster


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, "Бот запущен")


def register_global_middlewares(dp: Dispatcher, config: Config, session_pool=None):
    """
    Регистрация глобальных middleware для указанного диспетчера.
    Здесь глобальные middleware - это те, которые применяются ко всем обработчикам (вы указываете тип обновления)

    :param dp: Экземпляр диспетчера.
    :type dp: Dispatcher
    :param config: Объект конфигурации из загруженной конфигурации.
    :param session_pool: Необязательный объект пула сессий для базы данных с использованием SQLAlchemy.
    :return: None
    """
    middleware_types = [
        ConfigMiddleware(config),
        # DatabaseMiddleware(session_pool),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)


def setup_logging():
    """
    Настройка конфигурации логирования для приложения.

    Этот метод инициализирует конфигурацию логирования для приложения.
    Он устанавливает уровень журнала на INFO и настраивает основной цветной журнал для
    вывода. Формат журнала включает имя файла, номер строки, уровень журнала,
    отметку времени, имя логгера и сообщение журнала.

    Возвращает:
        None

    Пример использования:
        setup_logging()
    """
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Запуск бота")


def get_storage(config):
    """
    Возвращает хранилище на основе предоставленной конфигурации.

    Args:
        config (Config): Объект конфигурации.

    Returns:
        Storage: Объект хранилища на основе конфигурации.

    """
    if config.tg_bot.use_redis:
        return RedisStorage.from_url(
            config.redis.dsn(),
            key_builder=DefaultKeyBuilder(with_bot_id=True, with_destiny=True),
        )
    else:
        return MemoryStorage()


async def main():
    setup_logging()

    config = load_config(".env")
    storage = get_storage(config)

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)

    dp.include_routers(*routers_list)

    register_global_middlewares(dp, config)

    await on_startup(bot, config.tg_bot.admin_ids)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот был выключен!")
