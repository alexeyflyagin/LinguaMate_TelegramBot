from dependency_injector import containers, providers

from src.base.http_client import HTTPClient
from src.data.session_manager import SessionManager


class DataContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    session_manager = providers.Singleton(
        SessionManager,
        db_url=config.DB_URL
    )

    lingua_mate_http_client = providers.Singleton(
        HTTPClient,
        base_url=config.LINGUAMATE_API__URL
    )
