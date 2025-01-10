from typing import Dict, Any, Optional

from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType

from src.services.user_state import UserStateService


class PgSQLUserStateStorage(BaseStorage):

    def __init__(self, user_state_service: UserStateService):
        self.user_state_service = user_state_service

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        await self.user_state_service.set_state(key, state)

    async def get_state(self, key: StorageKey) -> Optional[str]:
        return await self.user_state_service.get_state(key)

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        await self.user_state_service.set_data(key, data)

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        return await self.user_state_service.get_data(key)

    async def close(self) -> None:
        pass
