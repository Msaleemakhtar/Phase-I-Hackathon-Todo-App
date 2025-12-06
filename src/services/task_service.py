"""Task business logic and storage operations."""

from src.constants import ERROR_INVALID_TASK_ID, ERROR_TASK_NOT_FOUND
from src.models.task import Task

# In-memory task storage (ephemeral)
_task_storage: list[Task] = []


def generate_next_id() -> int:
    """Generate the next sequential task ID.

    Returns:
        1 if task list is empty, otherwise max(existing IDs) + 1
    """
    if not _task_storage:
        return 1
    return max(task.id for task in _task_storage) + 1


def create_task(title: str, description: str) -> Task:
    """Create and store a new task.

    Args:
        title: Task title (already validated)
        description: Task description (already validated, may be empty)

    Returns:
        Newly created Task instance
    """
    timestamp = Task.generate_timestamp()
    task = Task(
        id=generate_next_id(),
        title=title,
        description=description,
        completed=False,
        created_at=timestamp,
        updated_at=timestamp,
    )
    _task_storage.append(task)
    return task


def get_all_tasks() -> list[Task]:
    """Retrieve all tasks from storage.

    Returns:
        List of all Task instances (may be empty)
    """
    return _task_storage.copy()


def get_task_by_id(task_id: int) -> Task:
    """Retrieve a single task by its unique ID.

    Args:
        task_id: The unique identifier of the task to retrieve

    Returns:
        Task object with the matching ID

    Raises:
        ValueError: If task_id <= 0 (ERROR 103)
        ValueError: If no task with task_id exists (ERROR 101)
    """
    # Validate task_id is positive
    if task_id <= 0:
        raise ValueError(ERROR_INVALID_TASK_ID)

    # Search for task with matching ID
    for task in _task_storage:
        if task.id == task_id:
            return task

    # Task not found
    raise ValueError(ERROR_TASK_NOT_FOUND.format(task_id=task_id))
