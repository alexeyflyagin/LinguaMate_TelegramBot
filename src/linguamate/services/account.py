from uuid import UUID

import aiohttp

from src.base.http_client import HTTPClient
from src.linguamate.exceptions import LinguaMateAPIError, LinguaMateBadRequestError, \
    LinguaMateNetworkError, LinguaMateInvalidTokenError
from src.linguamate.models.account import AccountInfoResponse
from src.linguamate.services.utils import unexpected_error_log_text, default_check_status_codes
from src.loggers import service_logger


class AccountService:

    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    async def get_info(self, token: UUID) -> AccountInfoResponse:
        """
        :raises LinguaMateInvalidTokenError:
        :raises LinguaMateBadRequestError:
        :raises LinguaMateNetworkError:
        :raises LinguaMateAPIError: Unexpected errors
        """
        try:
            async with await self._http_client.session as s:
                try:
                    response = await s.get(url=f'/{str(token)}/account/getInfo')
                except aiohttp.ClientError as e:
                    raise LinguaMateNetworkError(e)
                res_json = await response.json()
                default_check_status_codes(response.status, res_json)
                if response.status == 200:
                    return AccountInfoResponse.model_validate(res_json)
        except LinguaMateInvalidTokenError as e:
            service_logger.debug(e)
            raise
        except (LinguaMateBadRequestError, LinguaMateNetworkError) as e:
            service_logger.error(e)
            raise
        except Exception as e:
            service_logger.exception(unexpected_error_log_text(e))
            raise LinguaMateAPIError(str(e))
