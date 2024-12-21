'Собирает все роутеры во-едино'

# Импортируем все обработчики
from handlers import (
    start,
    all_msg
)

routers = (
    start.router,
    all_msg.router
)

__all__ = ("routers",)
