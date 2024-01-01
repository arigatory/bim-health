from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from infrastructure.excel import make_report
from infrastructure.postgres import get_name_record
from tgbot.filters.admin import AdminFilter
from aiogram.filters import Command


admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    telegram_id = message.from_user.id
    telegram_nickname = message.from_user.username

    record = get_name_record(telegram_id, telegram_nickname)

    if record:
        if record.real_name:
            await message.reply(f"Приветствую, {record.real_name}!")
            return
        if record.nickname:
            await message.reply(f"Приветствую, {record.nickname}!")
            return

        await message.reply("Приветствую, администратор!")


@admin_router.message(Command("report"))
async def excel_report(message: Message):
    # Генерируем Excel-файл
    make_report()
    document = FSInputFile("Records.xlsx")
    await message.answer_document(document, caption="Ваш отчет по здоровью")
