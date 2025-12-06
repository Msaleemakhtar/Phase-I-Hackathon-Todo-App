"""User input prompts and validation."""

from src.constants import (
    ERROR_DESCRIPTION_TOO_LONG,
    ERROR_INVALID_INPUT,
    ERROR_INVALID_TASK_ID,
    ERROR_TITLE_REQUIRED,
    ERROR_TITLE_TOO_LONG,
    MAX_DESCRIPTION_LENGTH,
    MAX_TITLE_LENGTH,
    MSG_NO_TASKS,
    PROMPT_DESCRIPTION,
    PROMPT_PAGINATION,
    PROMPT_TASK_ID,
    PROMPT_TITLE,
)
from src.models.task import Task


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


def display_task_list(tasks: list[Task]) -> None:
    """Display a formatted list of all tasks with completion indicators and pagination.

    Args:
        tasks: List of Task objects to display (may be empty)

    Behavior:
        - If tasks is empty: Display "No tasks found." and return
        - For each task: Display "{id}. [{indicator}] {title}"
          where indicator is "[X]" if completed, "[ ]" if not
        - After every 20 tasks (if more tasks remain): Display "Press Enter to continue..."
          and wait for user input
        - After all tasks: Display "Total: {count} tasks"
    """
    if not tasks:
        print(MSG_NO_TASKS)
        return

    for index, task in enumerate(tasks, start=1):
        indicator = "[X]" if task.completed else "[ ]"
        print(f"{task.id}. {indicator} {task.title}")

        # Pagination: pause every 20 tasks if more remain
        if index % 20 == 0 and index < len(tasks):
            input(PROMPT_PAGINATION)

    # Display task count summary
    count = len(tasks)
    task_word = "task" if count == 1 else "tasks"
    print(f"\nTotal: {count} {task_word}")


def display_task_details(task: Task) -> None:
    """Display detailed information for a single task with all fields labeled.

    Args:
        task: The Task object to display in detail

    Behavior:
        - Display all 6 task fields with labels
        - Empty descriptions show "(No description)" placeholder
        - Completed field shows "Yes" or "No" (not True/False)
        - Timestamps displayed in ISO 8601 format as-is
    """
    # Handle empty description
    description = task.description.strip() if task.description.strip() else "(No description)"

    # Format completed status
    completed_status = "Yes" if task.completed else "No"

    # Display all fields with labels
    print(f"ID: {task.id}")
    print(f"Title: {task.title}")
    print(f"Description: {description}")
    print(f"Completed: {completed_status}")
    print(f"Created At: {task.created_at}")
    print(f"Updated At: {task.updated_at}")


def prompt_for_task_id() -> int:
    """Prompt user to enter a task ID and validate it's a positive integer.

    Returns:
        Valid positive task ID entered by user

    Raises:
        ValueError: If input is non-numeric (ERROR 102)
        ValueError: If input is zero or negative (ERROR 103)
    """
    user_input = input(PROMPT_TASK_ID)

    # Validate input is numeric
    try:
        task_id = int(user_input)
    except ValueError:
        raise ValueError(ERROR_INVALID_INPUT)

    # Validate input is positive
    if task_id <= 0:
        raise ValueError(ERROR_INVALID_TASK_ID)

    return task_id
