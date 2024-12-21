'Модуль для парсинга codewars.com'

import requests
import matplotlib.pyplot as plt
from datetime import datetime
from loguru import logger

from utils.exceptions import UserNotFoundError


def get_page(session: requests.Session, username: str) -> requests.Response:
    'Пагинация'

    page_counter = 0

    while True:

        resp = session.get((
            f'https://www.codewars.com/api/v1/users/{username}'
            f'/code-challenges/completed?page={page_counter}'
        ))
        if resp.status_code == 200:
            yield resp
            logger.debug('Обработана страница {}', page_counter)
            page_counter += 1
        elif resp.status_code == 404:
            raise UserNotFoundError()
        else:
            logger.error(f'Ошибка  {resp.status_code}: {resp=}')
            break


def get_data_from_codewars(username: str):
    'Получает информацию с codewars.com'

    dates = []
    with requests.Session() as session:
        for page_resp in get_page(session, username):
            page_json = page_resp.json()
            if not page_json['data']:
                break

            for j in page_json['data']:
                date_str = j['completedAt']
                date_object = datetime.strptime(
                    date_str, '%Y-%m-%dT%H:%M:%S.%fZ'
                )
                dates.append(date_object)
    return dates


async def get_graph(username: str) -> None:
    'Строит график'

    try:
        dates = get_data_from_codewars(username)
        dates.sort()

        # Построение графика
        plt.figure(figsize=(10, 6))
        plt.plot(dates, range(len(dates)))
        plt.xlabel('Дата')
        plt.ylabel('Количество решенных задач')
        plt.title(f'Прогресс пользователя {username} на Codewars')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'images/{username}_graph.png')

        return True, 'ok'

    except UserNotFoundError:
        return False, 'пользователь не найден'

    except Exception as e:
        return False, f'{e}'
