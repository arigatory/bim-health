from dataclasses import dataclass
import uuid
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from infrastructure.postgres import get_name_record


user_router = Router()


@dataclass
class NameRecord:
    id: uuid.UUID
    telegram_id: int
    nickname: str
    real_name: str


@user_router.message(CommandStart())
async def user_start(message: Message):
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

        await message.reply("Приветствую, обычный пользователь!")
