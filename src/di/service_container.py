from uuid import UUID

from dependency_injector import containers, providers

from src.linguamate.services.account import AccountService
from src.linguamate.services.auth import AuthService
from src.linguamate.services.phrase import PhraseService
from src.services.user_state import UserStateService


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    data_container = providers.DependenciesContainer()

    user_state_service = providers.Factory(
        UserStateService,
        session_manager=data_container.session_manager
    )

    auth_service = providers.Factory(
        AuthService,
        http_client=data_container.lingua_mate_http_client,
        trusted_key=config.LINGUAMATE_API__TRUSTED_KEY,
    )

    account_service = providers.Factory(
        AccountService,
        http_client=data_container.lingua_mate_http_client,
    )

    phrase_service = providers.Factory(
        PhraseService,
        http_client=data_container.lingua_mate_http_client,
    )
