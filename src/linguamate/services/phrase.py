from uuid import UUID

import aiohttp

from src.base.http_client import HTTPClient
from src.linguamate.exceptions import LinguaMateAPIError, LinguaMateNotFoundError, LinguaMateBadRequestError, \
    LinguaMateNetworkError, LinguaMateConflictError, LinguaMateInvalidTokenError
from src.linguamate.models.auth import AuthData, AuthResponse, SignupData, CheckTokenResponse
from src.linguamate.models.phrase import AddPhraseData, AddPhraseResponse, AddPhrasesData, AddPhrasesResponse
from src.linguamate.services.utils import unexpected_error_log_text, default_check_status_codes
from src.loggers import service_logger


class PhraseService:

    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    async def add_phrase(self, token: UUID, data: AddPhraseData) -> AddPhraseResponse:
        """
        :raises LinguaMateConflictError: The phrase already exists.
        :raises LinguaMateInvalidTokenError:
        :raises LinguaMateBadRequestError:
        :raises LinguaMateNetworkError:
        :raises LinguaMateAPIError: Unexpected errors
        """
        try:
            async with await self._http_client.session as s:
                try:
                    response = await s.post(url=f'/{str(token)}/phrasebook/addPhrase/', json=data.model_dump())
                except aiohttp.ClientError as e:
                    raise LinguaMateNetworkError(e)
                res_json = await response.json()
                default_check_status_codes(response.status, res_json, ignore=[409])
                if response.status == 200:
                    return AddPhraseResponse.model_validate(res_json)
                elif response.status == 409:
                    raise LinguaMateConflictError(f"This phrase ('{data.phrase}') already exists.")
        except (LinguaMateInvalidTokenError, LinguaMateConflictError) as e:
            service_logger.debug(e)
            raise
        except (LinguaMateBadRequestError, LinguaMateNetworkError) as e:
            service_logger.error(e)
            raise
        except Exception as e:
            service_logger.exception(unexpected_error_log_text(e))
            raise LinguaMateAPIError(str(e))

    async def add_phrases(self, token: UUID, data: AddPhrasesData) -> AddPhrasesResponse:
        """
        :raises LinguaMateInvalidTokenError:
        :raises LinguaMateBadRequestError:
        :raises LinguaMateNetworkError:
        :raises LinguaMateAPIError: Unexpected errors
        """
        try:
            async with await self._http_client.session as s:
                try:
                    response = await s.post(url=f'/{str(token)}/phrasebook/addPhrases/', json=data.model_dump())
                except aiohttp.ClientError as e:
                    raise LinguaMateNetworkError(e)
                res_json = await response.json()
                default_check_status_codes(response.status, res_json)
                if response.status == 200:
                    return AddPhrasesResponse.model_validate(res_json)
        except LinguaMateInvalidTokenError as e:
            service_logger.debug(e)
            raise
        except (LinguaMateBadRequestError, LinguaMateNetworkError) as e:
            service_logger.error(e)
            raise
        except Exception as e:
            service_logger.exception(unexpected_error_log_text(e))
            raise LinguaMateAPIError(str(e))
