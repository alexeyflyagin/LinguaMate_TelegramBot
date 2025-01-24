from uuid import UUID

import aiohttp

from src.base.http_client import HTTPClient
from src.linguamate.exceptions import LinguaMateAPIError, LinguaMateNotFoundError, LinguaMateBadRequestError, \
    LinguaMateNetworkError, LinguaMateConflictError, LinguaMateInvalidTokenError, LinguaMateInvalidTrustedKeyError
from src.linguamate.models.auth import AuthData, AuthResponse, SignupData, CheckTokenResponse
from src.linguamate.services.utils import unexpected_error_log_text, default_check_status_codes
from src.loggers import service_logger


class AuthService:

    def __init__(self, http_client: HTTPClient, trusted_key: UUID):
        self.trusted_key = trusted_key
        self._http_client = http_client

    async def auth(self, data: AuthData) -> AuthResponse:
        """
        :raises LinguaMateNotFoundError: Account not found
        :raises LinguaMateInvalidTrustedKeyError: If the trusted key is invalid
        :raises LinguaMateBadRequestError:
        :raises LinguaMateNetworkError:
        :raises LinguaMateAPIError: Unexpected errors
        """
        try:
            async with await self._http_client.session as s:
                try:
                    response = await s.post(url=f'/{str(self.trusted_key)}/auth/', json=data.model_dump())
                except aiohttp.ClientError as e:
                    raise LinguaMateNetworkError(e)
                res_json = await response.json()
                default_check_status_codes(response.status, res_json, ignore=[404, 403])
                if response.status == 200:
                    return AuthResponse.model_validate(res_json)
                elif response.status == 403:
                    raise LinguaMateInvalidTrustedKeyError()
                elif response.status == 404:
                    raise LinguaMateNotFoundError("Account not found.")
        except LinguaMateNotFoundError as e:
            service_logger.debug(e)
            raise
        except (LinguaMateBadRequestError, LinguaMateNetworkError) as e:
            service_logger.error(e)
            raise
        except LinguaMateInvalidTrustedKeyError as e:
            service_logger.critical(e)
            raise
        except Exception as e:
            service_logger.exception(unexpected_error_log_text(e))
            raise LinguaMateAPIError(str(e))

    async def signup(self, data: SignupData):
        """
        :raises LinguaMateInvalidTrustedKeyError: If the trusted key is invalid
        :raises LinguaMateConflictError: If account already exists
        :raises LinguaMateBadRequestError:
        :raises LinguaMateNetworkError:
        :raises LinguaMateAPIError: Unexpected errors
        """
        try:
            async with await self._http_client.session as s:
                try:
                    response = await s.post(url=f'/{self.trusted_key}/signup/', json=data.model_dump())
                except aiohttp.ClientError as e:
                    raise LinguaMateNetworkError(e)
                res_json = await response.json()
                default_check_status_codes(response.status, res_json, ignore=[409, 403])
                if response.status == 200:
                    return
                elif response.status == 403:
                    raise LinguaMateInvalidTrustedKeyError()
                elif response.status == 409:
                    raise LinguaMateConflictError("Account already exists.")
        except LinguaMateConflictError as e:
            service_logger.debug(e)
            raise
        except (LinguaMateBadRequestError, LinguaMateNetworkError) as e:
            service_logger.error(e)
            raise
        except LinguaMateInvalidTrustedKeyError as e:
            service_logger.critical(e)
            raise
        except Exception as e:
            service_logger.exception(unexpected_error_log_text(e))
            raise LinguaMateAPIError(str(e))

    async def check_token(self, token: UUID, raise_if_none: bool = True) -> CheckTokenResponse:
        """
        :param token:
        :param raise_if_none: raise LinguaMateInvalidTokenError if it's True and token is not valid

        :raises LinguaMateInvalidTrustedKeyError: If the trusted key is invalid
        :raises LinguaMateInvalidTokenError:
        :raises LinguaMateBadRequestError:
        :raises LinguaMateNetworkError:
        :raises LinguaMateAPIError: Unexpected errors
        """
        try:
            async with await self._http_client.session as s:
                try:
                    response = await s.get(url=f'/{str(self.trusted_key)}/{str(token)}/checkToken/')
                except aiohttp.ClientError as e:
                    raise LinguaMateNetworkError(e)
                res_json = await response.json()
                default_check_status_codes(response.status, res_json=[403])
                if response.status == 200:
                    res = CheckTokenResponse.model_validate(res_json)
                    if not res.is_valid and raise_if_none:
                        raise LinguaMateInvalidTokenError(response)
                    return res
                elif response.status == 403:
                    raise LinguaMateInvalidTrustedKeyError()
        except LinguaMateInvalidTokenError as e:
            service_logger.debug(e)
            raise
        except (LinguaMateBadRequestError, LinguaMateNetworkError) as e:
            service_logger.error(e)
            raise
        except LinguaMateInvalidTrustedKeyError as e:
            service_logger.critical(e)
            raise
        except Exception as e:
            service_logger.exception(unexpected_error_log_text(e))
            raise LinguaMateAPIError(str(e))
