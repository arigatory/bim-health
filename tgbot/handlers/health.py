from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from infrastructure import postgres

from tgbot.keyboards.inline import simple_menu_keyboard

menu_router = Router()


@menu_router.message(Command("health"))
async def show_menu(message: Message):
    await message.answer("Как ваше здоровье:", reply_markup=simple_menu_keyboard())


@menu_router.callback_query(F.data == "healthy")
async def write_healthy(query: CallbackQuery):
    # В первую очередь всегда отвечаем на callback-запрос (как требует API Telegram)
    await query.answer()

    user_id = query.from_user.id
    nickname = query.from_user.username
    health_status = "Здоров"
    postgres.insert_data(user_id, nickname, health_status)

    await query.message.answer("Вы здоровы, это прекрасно!")
    await query.message.answer("Если что-то поменяется, можете в любое время поменять свой статус:",
                               reply_markup=simple_menu_keyboard())


@menu_router.callback_query(F.data == "ill")
async def write_ill(query: CallbackQuery):

    user_id = query.from_user.id
    nickname = query.from_user.username
    health_status = "Болен"
    postgres.insert_data(user_id, nickname, health_status)
    await query.answer()
    await query.message.answer("Как жаль, что вы заболели... Поскорее выздоравливайте!")
    await query.message.answer("Держите в курсе руководителя относительно текущего состояния")
    await query.message.answer("Если что-то поменяется, можете в любое время поменять свой статус:",
                               reply_markup=simple_menu_keyboard())


@menu_router.callback_query(F.data == "recover")
async def write_recover(query: CallbackQuery):
    user_id = query.from_user.id
    nickname = query.from_user.username
    health_status = "Почти выздоровел"
    postgres.insert_data(user_id, nickname, health_status)

    await query.answer()
    await query.message.answer("Вирус может быть коварен, не переставайте лечиться!")
    await query.message.answer("Если что-то поменяется, можете в любое время поменять свой статус:",
                               reply_markup=simple_menu_keyboard())
