from aiohttp import ClientSession


class HTTPClient:
    def __init__(self, base_url: str):
        self._base_url = base_url

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    async def session(self) -> ClientSession:
        return ClientSession(base_url=self.base_url)
