MARKDOWN_V1_CHARS = r"_*[]()"


def esc_md(text: str) -> str:
    """
    It allows escaping MARKDOWN V1.
    """
    if not (isinstance(text, str)):
        raise ValueError(f"The value types is incorrect (text={type(text)}")

    for char in MARKDOWN_V1_CHARS:
        text = text.replace(char, f"\\{char}")
    return text


def add_counter(text: str, count: int, pattern: str = '{text} ({count})') -> str:
    """
    It adds `count` into the `text`.

    **Default pattern**: `{text} ({count})`

    Example:
        >> add_counter("Some text", 23)\n
        << "Some text (23)"
    """

    if not (isinstance(text, str) and isinstance(count, int) and isinstance(pattern, str)):
        raise ValueError(
            f"The value types is incorrect (text={type(text)}, count={type(count)}, pattern={type(pattern)})")

    if not ('{text}' in pattern and '{count}' in pattern):
        raise ValueError(f"The pattern is incorrect (pattern=\"{pattern}\")")

    return pattern.format(text=text, count=count)
