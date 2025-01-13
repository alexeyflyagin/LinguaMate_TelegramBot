from dependency_injector import containers, providers

import src.bot.handlers.auth
from src import config
from src.di.bot_container import BotContainer
from src.di.data_container import DataContainer
from src.di.service_container import ServiceContainer


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    data: DataContainer = providers.Container(DataContainer, config=config)
    service: ServiceContainer = providers.Container(ServiceContainer, data_container=data)
    bot: BotContainer = providers.Container(BotContainer, config=config, service_container=service)


di = AppContainer()

di.config.BOT_TOKEN.from_value(config.BOT_TOKEN)
di.config.DB_URL.from_value(config.DB_URL)
di.config.LINGUA_MATE_API_URL.from_value(config.LINGUAMATE_API_URL)

src.bot.handlers.auth.auth_service = di.service.auth_service()
