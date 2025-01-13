import aiohttp

from src.base.http_client import HTTPClient
from src.linguamate.exceptions import LinguaMateAPIError, LinguaMateNotFoundError, LinguaMateBadRequestError, \
    UnexpectedStatusError, LinguaMateNetworkError, LinguaMateConflictError
from src.linguamate.models.auth import AuthData, AuthResponse, SignupData
from src.linguamate.services.utils import unexpected_error_log_text
from src.loggers import logger


class AuthService:

    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    async def auth(self, data: AuthData) -> AuthResponse:
        """
        :raises LinguaMateNotFoundError: Account not found
        :raises LinguaMateBadRequestError:
        :raises LinguaMateNetworkError:
        :raises LinguaMateAPIError: Unexpected errors
        """
        try:
            async with await self._http_client.session as s:
                try:
                    response = await s.post(url=f'/auth/', json=data.model_dump())
                except aiohttp.ClientError as e:
                    raise LinguaMateNetworkError(e)
                res_json = await response.json()
                if response.status == 200:
                    return AuthResponse.model_validate(res_json)
                elif response.status == 404:
                    raise LinguaMateNotFoundError("Account not found.")
                elif response.status == 422:
                    raise LinguaMateBadRequestError(res_json)
                else:
                    raise UnexpectedStatusError(response.status, res_json)
        except LinguaMateNotFoundError as e:
            logger.debug(e)
            raise
        except LinguaMateBadRequestError as e:
            logger.error(e)
            raise
        except LinguaMateNetworkError as e:
            logger.error(e)
            raise
        except Exception as e:
            logger.exception(unexpected_error_log_text(e))
            raise LinguaMateAPIError(str(e))

    async def signup(self, data: SignupData):
        """
        :raises LinguaMateConflictError: Account already exists.
        :raises LinguaMateBadRequestError:
        :raises LinguaMateNetworkError:
        :raises LinguaMateAPIError: Unexpected errors
        """
        try:
            async with await self._http_client.session as s:
                try:
                    response = await s.post(url=f'/signup/', json=data.model_dump())
                except aiohttp.ClientError as e:
                    raise LinguaMateNetworkError(e)
                res_json = await response.json()
                if response.status == 200:
                    return
                elif response.status == 409:
                    raise LinguaMateConflictError("Account already exists.")
                elif response.status == 422:
                    raise LinguaMateBadRequestError(res_json)
                else:
                    raise UnexpectedStatusError(response.status, res_json)
        except LinguaMateConflictError as e:
            logger.debug(e)
            raise
        except LinguaMateBadRequestError as e:
            logger.error(e)
            raise
        except LinguaMateNetworkError as e:
            logger.error(e)
            raise
        except Exception as e:
            logger.exception(unexpected_error_log_text(e))
            raise LinguaMateAPIError(str(e))
