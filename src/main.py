import asyncio
from asyncio import CancelledError

from src.bot.bot import LinguaMateBot
from src.di.app_container import di


async def main():
    bot: LinguaMateBot = di.bot.lingua_mate_bot()
    try:
        await di.data.session_manager().test_connection()
        await bot.run()
    except CancelledError:
        pass
    finally:
        await di.data.session_manager().disconnect()


if __name__ == '__main__':
    asyncio.run(main())
