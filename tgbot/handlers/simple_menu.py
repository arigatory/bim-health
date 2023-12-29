from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from tgbot.keyboards.inline import simple_menu_keyboard

menu_router = Router()


@menu_router.message(Command("health"))
async def show_menu(message: Message):
    await message.answer("Как ваше здоровье:", reply_markup=simple_menu_keyboard())

# Мы можем использовать фильтр F.data для фильтрации callback-запросов по полю data из объекта CallbackQuery


@menu_router.callback_query(F.data == "healthy")
async def write_healthy(query: CallbackQuery):
    # В первую очередь всегда отвечаем на callback-запрос (как требует API Telegram)
    await query.answer()

    # Этот метод отправит ответ на сообщение с кнопкой, которую нажал пользователь
    # Здесь query - это объект CallbackQuery, который содержит message: Message object
    await query.message.answer("Вы здоровы, это прекрасно!")
    await query.message.answer("Если что-то поменяется, можете в любое время поменять свой статус:",
                               reply_markup=simple_menu_keyboard())

    # Вы также можете отредактировать сообщение с новым текстом
    # await query.message.edit_text("Вы выбрали создание заказа!")


@menu_router.callback_query(F.data == "ill")
async def write_ill(query: CallbackQuery):
    await query.answer()
    await query.message.answer("Как жаль, что вы заболели... Поскорее выздоравливайте! Держите в курсе руководителя относительно текущего состояния")
    await query.message.answer("Если что-то поменяется, можете в любое время поменять свой статус:",
                               reply_markup=simple_menu_keyboard())

    # await query.message.edit_text("Вы выбрали просмотр ваших заказов.",
    #                               reply_markup=my_orders_keyboard(ORDERS))


@menu_router.callback_query(F.data == "recover")
async def write_recover(query: CallbackQuery):
    await query.answer()
    await query.message.answer("Вирус может быть коварен, не переставайте лечиться!")
    await query.message.answer("Если что-то поменяется, можете в любое время поменять свой статус:",
                               reply_markup=simple_menu_keyboard())
