import asyncio
import logging
import sys
from asyncio import CancelledError

from src.bot.bot import LinguaMateBot
from src.di.container import di

logging.getLogger('aiogram').setLevel(level=logging.CRITICAL)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

bot: LinguaMateBot = di.lingua_mate_bot()


async def main():
    try:
        await bot.run()
    except CancelledError:
        await di.session_manager().disconnect()


if __name__ == '__main__':
    asyncio.run(main())
