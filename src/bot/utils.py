MARKDOWN_V1_CHARS = r"_*[]()"


def esc_md(text: str) -> str:
    """
    It allows escaping MARKDOWN V1.
    """
    for char in MARKDOWN_V1_CHARS:
        text = text.replace(char, f"\\{char}")
    return text
