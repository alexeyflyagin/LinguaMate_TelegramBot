from dependency_injector import containers, providers

from src import config
from src.bot import handlers
from src.di.bot_container import BotContainer
from src.di.data_container import DataContainer
from src.di.service_container import ServiceContainer


def inject_into_routers():
    handlers.auth.auth_service = di.service.auth_service()

    handlers.fast_phrase.auth_service = di.service.auth_service()
    handlers.fast_phrase.phrase_service = di.service.phrase_service()

    handlers.add_phrase_mode.auth_service = di.service.auth_service()
    handlers.add_phrase_mode.phrase_service = di.service.phrase_service()


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    data: DataContainer = providers.Container(DataContainer, config=config)
    service: ServiceContainer = providers.Container(ServiceContainer, config=config, data_container=data)
    bot: BotContainer = providers.Container(BotContainer, config=config, service_container=service)


di = AppContainer()

di.config.BOT_TOKEN.from_value(config.BOT_TOKEN)
di.config.DB_URL.from_value(config.DB_URL)
di.config.LINGUAMATE_API__URL.from_value(config.LINGUAMATE_API__URL)
di.config.LINGUAMATE_API__BOT_KEY.from_value(config.LINGUAMATE_API__BOT_KEY)

inject_into_routers()
