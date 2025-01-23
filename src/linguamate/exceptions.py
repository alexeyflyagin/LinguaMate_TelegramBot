class LinguaMateAPIError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class UnexpectedStatusError(Exception):
    def __init__(self, status_code: int, response):
        super().__init__(f"Unexpected status code {status_code}: {response}")


class LinguaMateNetworkError(LinguaMateAPIError):
    def __init__(self, e: Exception):
        super().__init__(f"A network error occurred: {e}")


class LinguaMateNotFoundError(LinguaMateAPIError):
    def __init__(self, *args):
        super().__init__(*args)


class LinguaMateConflictError(LinguaMateAPIError):
    def __init__(self, *args):
        super().__init__(*args)


class LinguaMateForbiddenError(LinguaMateAPIError):
    def __init__(self, *args):
        super().__init__(*args)


class LinguaMateInvalidTrustedKeyError(LinguaMateForbiddenError):
    def __init__(self):
        super().__init__("The trusted key is invalid.")


class LinguaMateBadRequestError(LinguaMateAPIError):
    def __init__(self, response):
        super().__init__(f"A bad request error occurred. Response: {response}")


class LinguaMateInvalidTokenError(LinguaMateAPIError):
    def __init__(self, response):
        super().__init__(f"The token is incorrect. Response: {response}")
