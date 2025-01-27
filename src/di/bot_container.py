from dependency_injector import containers, providers

from src.bot.bot import LinguaMateBot
from src.bot.user_state_storage import PgSQLUserStateStorage


class BotContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    service_container = providers.DependenciesContainer()

    user_state_storage = providers.Factory(
        PgSQLUserStateStorage,
        user_state_service=service_container.user_state_service
    )

    lingua_mate_bot = providers.Factory(
        LinguaMateBot,
        token=config.BOT_TOKEN,
        storage=user_state_storage
    )
