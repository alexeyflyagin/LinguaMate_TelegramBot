from dependency_injector import containers, providers

from src.linguamate.services.auth import AuthService
from src.services.user_state import UserStateService


class ServiceContainer(containers.DeclarativeContainer):
    data_container = providers.DependenciesContainer()

    user_state_service = providers.Factory(
        UserStateService,
        session_manager=data_container.session_manager
    )

    auth_service = providers.Factory(
        AuthService,
        http_client=data_container.lingua_mate_http_client,
    )
