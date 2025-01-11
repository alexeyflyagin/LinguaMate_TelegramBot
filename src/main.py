import asyncio
from asyncio import CancelledError

from src.bot.bot import LinguaMateBot
from src.di.container import di


async def main():
    bot: LinguaMateBot = di.lingua_mate_bot()
    try:
        await di.session_manager().test_connection()
        await bot.run()
    except CancelledError:
        pass
    finally:
        await di.session_manager().disconnect()


if __name__ == '__main__':
    asyncio.run(main())
