from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.base import BaseStorage

from src.bot import handlers
from src.loggers import logger


class LinguaMateBot:

    def __init__(
            self,
            token: str,
            storage: BaseStorage | None = None
    ):
        self.bot = Bot(token)
        self.dp = Dispatcher(storage=storage)
        self.dp.include_router(handlers.auth.router)
        self.dp.startup.register(self._startup)
        self.dp.shutdown.register(self._shutdown)

    async def _startup(self):
        bot_name = await self.bot.get_my_name()
        logger.info(f'{bot_name.name} bot is started.')

    async def _shutdown(self):
        bot_name = await self.bot.get_my_name()
        logger.info(f'{bot_name.name} bot is ended.')

    async def run(self):
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)
