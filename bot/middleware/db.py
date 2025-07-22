from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Any, Dict
from aiogram.types import Message

class DBMiddleware(BaseMiddleware):
    """
    Данный класс позволяет автоматически добавлять пулл соединений в хэндлеры.
    """
    def __init__(self, pool):
        super().__init__()
        self.pool = pool
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        data['pool'] = self.pool
        return await handler(event, data)
