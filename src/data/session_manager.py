from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


class SessionManager:

    def __init__(self, db_url: str):
        self._engine = create_async_engine(db_url)
        self._session_maker = async_sessionmaker(self._engine)

    @property
    def session(self) -> AsyncSession:
        return self._session_maker()
    
    async def disconnect(self):
        await self._engine.dispose()
