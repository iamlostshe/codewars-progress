'Информация о пользователе'

from aiogram import Router, F
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile

from utils.pars import get_graph

router = Router(name=__name__)


@router.message(F.text)
async def start_msg(msg: Message) -> None:
    'Обработка всех входящих сообщений'

    await msg.answer('Загружаю статистику с codewars.com...')

    graph = await get_graph(msg.text)

    if graph[0]:
        photo = FSInputFile(f'images/{msg.text}_graph.png')
        await msg.answer_photo(
            photo=photo,
            caption='Вот ваша статистика:'
        )
    else:
        await msg.answer(f'Произошла ошибка во время парсинга: {graph[1]}')
