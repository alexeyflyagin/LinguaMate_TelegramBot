from uuid import UUID

import aiohttp

from src.base.http_client import HTTPClient
from src.linguamate.exceptions import LinguaMateAPIError, LinguaMateNotFoundError, LinguaMateBadRequestError, \
    LinguaMateNetworkError, LinguaMateConflictError, LinguaMateInvalidTokenError
from src.linguamate.models.word import AddWordResponse, AddWordData, AddWordsData, AddWordsResponse, WordEntity, \
    GetWordFlowResponse
from src.linguamate.services.utils import unexpected_error_log_text, default_check_status_codes
from src.loggers import service_logger


class DictionaryService:

    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    async def add_word(self, token: UUID, data: AddWordData) -> AddWordResponse:
        """
        :raises LinguaMateConflictError: The word already exists
        :raises LinguaMateInvalidTokenError:
        :raises LinguaMateBadRequestError:
        :raises LinguaMateNetworkError:
        :raises LinguaMateAPIError: Unexpected errors
        """
        try:
            async with await self._http_client.session as s:
                try:
                    response = await s.post(url=f'/{str(token)}/dictionary/addWord/', json=data.model_dump())
                except aiohttp.ClientError as e:
                    raise LinguaMateNetworkError(e)
                res_json = await response.json()
                default_check_status_codes(response.status, res_json, ignore=[409])
                if response.status == 200:
                    return AddWordResponse.model_validate(res_json)
                elif response.status == 409:
                    raise LinguaMateConflictError(f"This word ('{data.word}') already exists.")
        except (LinguaMateInvalidTokenError, LinguaMateConflictError) as e:
            service_logger.debug(e)
            raise
        except (LinguaMateBadRequestError, LinguaMateNetworkError) as e:
            service_logger.error(e)
            raise
        except Exception as e:
            service_logger.exception(unexpected_error_log_text(e))
            raise LinguaMateAPIError(str(e))

    async def add_words(self, token: UUID, data: AddWordsData) -> AddWordsResponse:
        """
        :raises LinguaMateInvalidTokenError:
        :raises LinguaMateBadRequestError:
        :raises LinguaMateNetworkError:
        :raises LinguaMateAPIError: Unexpected errors
        """
        try:
            async with await self._http_client.session as s:
                try:
                    response = await s.post(url=f'/{str(token)}/dictionary/addWords/', json=data.model_dump())
                except aiohttp.ClientError as e:
                    raise LinguaMateNetworkError(e)
                res_json = await response.json()
                default_check_status_codes(response.status, res_json)
                if response.status == 200:
                    return AddWordsResponse.model_validate(res_json)
        except LinguaMateInvalidTokenError as e:
            service_logger.debug(e)
            raise
        except (LinguaMateBadRequestError, LinguaMateNetworkError) as e:
            service_logger.error(e)
            raise
        except Exception as e:
            service_logger.exception(unexpected_error_log_text(e))
            raise LinguaMateAPIError(str(e))

    async def get_word_by_id(self, token: UUID, word_id: int) -> WordEntity:
        """
        :raises LinguaMateNotFoundError: If the word was not found
        :raises LinguaMateInvalidTokenError:
        :raises LinguaMateBadRequestError:
        :raises LinguaMateNetworkError:
        :raises LinguaMateAPIError: Unexpected errors
        """
        try:
            async with await self._http_client.session as s:
                try:
                    response = await s.get(url=f'/{str(token)}/dictionary/getWordById',
                                           params={'word_id': word_id})
                except aiohttp.ClientError as e:
                    raise LinguaMateNetworkError(e)
                res_json = await response.json()
                default_check_status_codes(response.status, res_json, ignore=[404])
                if response.status == 200:
                    return WordEntity.model_validate(res_json)
                elif response.status == 404:
                    raise LinguaMateNotFoundError("The word was not found.")
        except (LinguaMateInvalidTokenError, LinguaMateNotFoundError) as e:
            service_logger.debug(e)
            raise
        except (LinguaMateBadRequestError, LinguaMateNetworkError) as e:
            service_logger.error(e)
            raise
        except Exception as e:
            service_logger.exception(unexpected_error_log_text(e))
            raise LinguaMateAPIError(str(e))

    async def get_word_flow(self, token: UUID) -> GetWordFlowResponse:
        """
        :raises LinguaMateNotFoundError: If a dictionary is empty
        :raises LinguaMateInvalidTokenError:
        :raises LinguaMateBadRequestError:
        :raises LinguaMateNetworkError:
        :raises LinguaMateAPIError: Unexpected errors
        """
        try:
            async with await self._http_client.session as s:
                try:
                    response = await s.get(url=f'/{str(token)}/dictionary/getWordFlow')
                except aiohttp.ClientError as e:
                    raise LinguaMateNetworkError(e)
                res_json = await response.json()
                default_check_status_codes(response.status, res_json, ignore=[404])
                if response.status == 200:
                    return GetWordFlowResponse.model_validate(res_json)
                elif response.status == 404:
                    raise LinguaMateNotFoundError("A dictionary is empty.")
        except (LinguaMateInvalidTokenError, LinguaMateNotFoundError) as e:
            service_logger.debug(e)
            raise
        except (LinguaMateBadRequestError, LinguaMateNetworkError) as e:
            service_logger.error(e)
            raise
        except Exception as e:
            service_logger.exception(unexpected_error_log_text(e))
            raise LinguaMateAPIError(str(e))
