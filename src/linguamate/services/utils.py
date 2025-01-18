from src.linguamate.exceptions import LinguaMateBadRequestError, UnexpectedStatusError, LinguaMateInvalidTokenError


def unexpected_error_log_text(e: Exception):
    return f"An unexpected error occurred: {e}"


def default_check_status_codes(status_code: int, res_json, ignore: list[int] | None = None):
    if not ignore:
        ignore = [200]
    if 200 not in ignore:
        ignore.append(200)
    if status_code in ignore:
        return
    if status_code == 422:
        raise LinguaMateBadRequestError(res_json)
    elif status_code == 401:
        raise LinguaMateInvalidTokenError(res_json)
    else:
        raise UnexpectedStatusError(status_code, res_json)
