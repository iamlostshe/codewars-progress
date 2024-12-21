'Приветственное сообщение'

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from utils import db


router = Router(name=__name__)


@router.message(CommandStart())
async def start_msg(msg: Message) -> None:
    'Обработка входящих комманд /start'

    await msg.answer(
        (
            f'👋 Привет, {msg.from_user.first_name}!\n\n'
            '⚙️ Этот бот нужен для получения удобной '
            'статистики в виде графика по прогрессу на codewars.com.\n\n'
            '📊 Для получения статистики ввдеи юзернейм '
            'пользователя с codewars.com'
        )
    )

    sourse = msg.text[7:]

    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    is_premium = msg.from_user.is_premium
    language_code = msg.from_user.language_code
    last_name = msg.from_user.last_name
    username = msg.from_user.username

    await db.add_user(
        user_id,
        sourse,
        first_name,
        last_name,
        is_premium,
        language_code,
        username
    )
