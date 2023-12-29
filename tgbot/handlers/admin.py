from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from infrastructure.excel import make_report
from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Приветствую, администратор!")


@admin_router.message()
async def excel_report(message: Message):
    # Генерируем Excel-файл
    make_report()
    document = FSInputFile("Records.xlsx")
    await message.answer_document(document, caption="Ваш отчет по здоровью")
