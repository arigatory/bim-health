from aiogram.utils.keyboard import InlineKeyboardBuilder


def simple_menu_keyboard():
    # Сначала создайте объект InlineKeyboardBuilder
    keyboard = InlineKeyboardBuilder()

    # Можно использовать метод keyboard.button() для добавления кнопок, затем введите текст и callback_data
    keyboard.button(
        text="😷 Болею",
        # В этом простом примере мы используем строку как callback_data
        callback_data="ill"
    )
    keyboard.button(
        text="❤️‍🩹 Выздоравливаю",
        # В этом простом примере мы используем строку как callback_data
        callback_data="recover"
    )

    keyboard.button(
        text="💚 Здоров",
        callback_data="healthy"
    )

    # При необходимости можно использовать метод keyboard.adjust() для изменения количества кнопок в строке
    keyboard.adjust(1)

    # Затем всегда нужно вызывать метод keyboard.as_markup(), чтобы получить действительный объект InlineKeyboardMarkup
    return keyboard.as_markup()
