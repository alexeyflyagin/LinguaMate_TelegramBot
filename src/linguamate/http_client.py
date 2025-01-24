from src.base.http_client import HTTPClient


class LinguaMateHTTPClient(HTTPClient):
    def __init__(self, base_url: str, timeout: int):
        super().__init__(base_url, timeout)
