from dependency_injector import containers, providers

from src.data.session_manager import SessionManager
from src.linguamate.http_client import LinguaMateHTTPClient


class DataContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    session_manager = providers.Singleton(
        SessionManager,
        db_url=config.DB_URL
    )

    lingua_mate_http_client = providers.Singleton(
        LinguaMateHTTPClient,
        base_url=config.LINGUAMATE_API__URL,
        timeout=60,
    )
