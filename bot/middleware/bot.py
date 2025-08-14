import asyncio

import asyncpg
from aiogram import (
    Bot,
    Dispatcher
)
from aiohttp import web


class State:
    def __init__(
            self,
            app: web.Application,
            bot: Bot,
            dp: Dispatcher,
            loop: asyncio.AbstractEventLoop
    ):
        self.app: web.Application = app
        self.bot = bot
        self.dp = dp
        self.loop: asyncio.AbstractEventLoop = loop
        self.db_pool: asyncpg.Pool | None = None
