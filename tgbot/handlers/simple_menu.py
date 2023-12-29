from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import as_section, as_key_value, as_marked_list

from tgbot.keyboards.inline import simple_menu_keyboard, my_orders_keyboard, \
    OrderCallbackData

menu_router = Router()

@menu_router.message(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Выберите пункт меню:", reply_markup=simple_menu_keyboard())

# Мы можем использовать фильтр F.data для фильтрации callback-запросов по полю data из объекта CallbackQuery
@menu_router.callback_query(F.data == "create_order")
async def create_order(query: CallbackQuery):
    # В первую очередь всегда отвечаем на callback-запрос (как требует API Telegram)
    await query.answer()

    # Этот метод отправит ответ на сообщение с кнопкой, которую нажал пользователь
    # Здесь query - это объект CallbackQuery, который содержит message: Message object
    await query.message.answer("Вы выбрали создание заказа!")

    # Вы также можете отредактировать сообщение с новым текстом
    # await query.message.edit_text("Вы выбрали создание заказа!")

# Давайте создадим простой список заказов для демонстрации
ORDERS = [
    {"id": 1, "title": "Заказ 1", "status": "В процессе выполнения"},
    {"id": 2, "title": "Заказ 2", "status": "Выполнен"},
    {"id": 3, "title": "Заказ 3", "status": "Выполнен"},
]

@menu_router.callback_query(F.data == "my_orders")
async def my_orders(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text("Вы выбрали просмотр ваших заказов.",
                                  reply_markup=my_orders_keyboard(ORDERS))

# Для фильтрации callback-данных, созданных с использованием фабрики CallbackData, вы можете использовать метод .filter()
@menu_router.callback_query(OrderCallbackData.filter())
async def show_order(query: CallbackQuery, callback_data: OrderCallbackData):
    await query.answer()

    # Вы можете получить данные из объекта callback_data в виде атрибутов
    order_id = callback_data.order_id

    # Затем вы можете получить заказ из вашей базы данных (здесь мы используем простой список)
    order_info = next((order for order in ORDERS if order["id"] == order_id), None)

    if order_info:
        # Здесь мы используем aiogram.utils.formatting для форматирования текста
        # https://docs.aiogram.dev/en/latest/utils/formatting.html
        text = as_section(
            as_key_value("Заказ #", order_info["id"]),
            as_marked_list(
                as_key_value("Товар", order_info["title"]),
                as_key_value("Статус", order_info["status"]),
            ),
        )
        # Пример:
        # Заказ #: 2
        # - Товар: Заказ 2
        # - Статус: Выполнен

        await query.message.edit_text(text.as_html(), parse_mode=ParseMode.HTML)

        # Вы также можете использовать MarkdownV2:
        # await query.message.edit_text(text.as_markdown(), parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await query.message.edit_text("Заказ не найден!")
