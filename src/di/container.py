from dependency_injector import containers, providers

from src import config
from src.bot.bot import LinguaMateBot
from src.bot.user_state_storage import PgSQLUserStateStorage
from src.data.session_manager import SessionManager
from src.services.user_state import UserStateService


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    session_manager = providers.Singleton(
        SessionManager,
        db_url=config.DB_URL
    )

    user_state_service = providers.Factory(
        UserStateService,
        session_manager=session_manager
    )

    user_state_storage = providers.Factory(
        PgSQLUserStateStorage,
        user_state_service=user_state_service
    )

    lingua_mate_bot = providers.Factory(
        LinguaMateBot,
        token=config.BOT_TOKEN,
        storage=user_state_storage
    )


di = AppContainer()

di.config.BOT_TOKEN.from_value(config.BOT_TOKEN)
di.config.DB_URL.from_value(config.DB_URL)
