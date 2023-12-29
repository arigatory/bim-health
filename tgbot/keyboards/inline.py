from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# Это простая клавиатура, содержащая 2 кнопки
def very_simple_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="📝 Создать заказ",
                                 callback_data="create_order"),
            InlineKeyboardButton(text="📋 Мои заказы", callback_data="my_orders"),
        ],
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )
    return keyboard


# Та же клавиатура, но созданная с использованием InlineKeyboardBuilder (предпочтительный способ)
def simple_menu_keyboard():
    # Сначала создайте объект InlineKeyboardBuilder
    keyboard = InlineKeyboardBuilder()

    # Можно использовать метод keyboard.button() для добавления кнопок, затем введите текст и callback_data
    keyboard.button(
        text="📝 Создать заказ",
        callback_data="create_order"
    )
    keyboard.button(
        text="📋 Мои заказы",
        # В этом простом примере мы используем строку как callback_data
        callback_data="my_orders"
    )

    # При необходимости можно использовать метод keyboard.adjust() для изменения количества кнопок в строке
    # keyboard.adjust(2)

    # Затем всегда нужно вызывать метод keyboard.as_markup(), чтобы получить действительный объект InlineKeyboardMarkup
    return keyboard.as_markup()


# Для более сложного использования callback_data можно использовать фабрику CallbackData
class OrderCallbackData(CallbackData, prefix="order"):
    """
    Этот класс представляет собой объект CallbackData для заказов.

    - При использовании в InlineKeyboardMarkup вы должны создать экземпляр этого класса, выполнить метод .pack() и передать его в параметр callback_data.

    - При использовании в InlineKeyboardBuilder вы должны создать экземпляр этого класса и передать его в параметр callback_data (без метода .pack()).

    - В обработчиках вы должны импортировать этот класс и использовать его в качестве фильтра для обработчиков callback query, а затем распаковать параметр callback_data, чтобы получить данные.

    # Пример использования в simple_menu.py
    """
    order_id: int


def my_orders_keyboard(orders: list):
    # Здесь мы используем список заказов в качестве параметра (из simple_menu.py)

    keyboard = InlineKeyboardBuilder()
    for order in orders:
        keyboard.button(
            text=f"📝 {order['title']}",
            # Здесь мы используем экземпляр класса OrderCallbackData в качестве параметра callback_data
            # order_id - это поле в классе OrderCallbackData, которое мы определили выше
            callback_data=OrderCallbackData(order_id=order["id"])
        )

    return keyboard.as_markup()
