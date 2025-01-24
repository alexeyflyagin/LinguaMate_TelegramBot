from aiohttp import ClientSession, ClientTimeout


class HTTPClient:
    def __init__(self, base_url: str, timeout: int = 60):
        self._base_url = base_url
        self._timeout = ClientTimeout(total=timeout)

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    async def session(self) -> ClientSession:
        return ClientSession(base_url=self.base_url, timeout=self._timeout)
