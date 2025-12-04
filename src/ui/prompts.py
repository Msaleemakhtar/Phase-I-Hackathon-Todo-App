"""User input prompts and validation."""

from src.constants import (
    ERROR_DESCRIPTION_TOO_LONG,
    ERROR_TITLE_REQUIRED,
    ERROR_TITLE_TOO_LONG,
    MAX_DESCRIPTION_LENGTH,
    MAX_TITLE_LENGTH,
    PROMPT_DESCRIPTION,
    PROMPT_TITLE,
)


def validate_title(title: str) -> tuple[bool, str | None]:
    """Validate task title according to specification rules.

    Args:
        title: Raw title input from user

    Returns:
        Tuple of (is_valid, error_message). error_message is None if valid.
    """
    stripped = title.strip()
    if len(stripped) == 0:
        return (False, ERROR_TITLE_REQUIRED)
    if len(stripped) > MAX_TITLE_LENGTH:
        return (False, ERROR_TITLE_TOO_LONG)
    return (True, None)


def validate_description(description: str) -> tuple[bool, str | None]:
    """Validate task description according to specification rules.

    Args:
        description: Raw description input from user

    Returns:
        Tuple of (is_valid, error_message). error_message is None if valid.
    """
    stripped = description.strip()
    if len(stripped) > MAX_DESCRIPTION_LENGTH:
        return (False, ERROR_DESCRIPTION_TOO_LONG)
    return (True, None)


def get_task_title() -> str:
    """Prompt user for task title with validation loop.

    Returns:
        Valid task title (stripped of leading/trailing whitespace)
    """
    while True:
        title = input(PROMPT_TITLE)
        is_valid, error = validate_title(title)
        if is_valid:
            return title.strip()
        print(error)


def get_task_description() -> str:
    """Prompt user for optional task description with validation loop.

    Returns:
        Valid task description (stripped, may be empty string)
    """
    while True:
        description = input(PROMPT_DESCRIPTION)
        is_valid, error = validate_description(description)
        if is_valid:
            return description.strip()
        print(error)
