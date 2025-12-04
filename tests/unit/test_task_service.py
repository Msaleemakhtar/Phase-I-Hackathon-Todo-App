"""Unit tests for task service operations."""

import pytest

from src.models.task import Task
from src.services import task_service


@pytest.fixture(autouse=True)
def reset_task_storage():
    """Reset task storage before each test."""
    task_service._task_storage.clear()
    yield
    task_service._task_storage.clear()


class TestGenerateNextId:
    """Tests for generate_next_id() function."""

    def test_generate_next_id_empty_storage(self):
        """Returns 1 when storage is empty."""
        next_id = task_service.generate_next_id()
        assert next_id == 1

    def test_generate_next_id_one_task(self):
        """Returns 2 when one task exists with ID 1."""
        task = Task(
            id=1,
            title="Test",
            description="",
            completed=False,
            created_at="2025-12-04T10:00:00.000000Z",
            updated_at="2025-12-04T10:00:00.000000Z",
        )
        task_service._task_storage.append(task)

        next_id = task_service.generate_next_id()
        assert next_id == 2

    def test_generate_next_id_multiple_tasks(self):
        """Returns max(ids) + 1 for multiple tasks."""
        tasks = [
            Task(
                1, "Task 1", "", False, "2025-12-04T10:00:00.000000Z", "2025-12-04T10:00:00.000000Z"
            ),
            Task(
                2, "Task 2", "", False, "2025-12-04T10:01:00.000000Z", "2025-12-04T10:01:00.000000Z"
            ),
            Task(
                3, "Task 3", "", False, "2025-12-04T10:02:00.000000Z", "2025-12-04T10:02:00.000000Z"
            ),
        ]
        task_service._task_storage.extend(tasks)

        next_id = task_service.generate_next_id()
        assert next_id == 4

    def test_generate_next_id_non_sequential(self):
        """Handles non-sequential IDs correctly (returns max + 1)."""
        tasks = [
            Task(
                1, "Task 1", "", False, "2025-12-04T10:00:00.000000Z", "2025-12-04T10:00:00.000000Z"
            ),
            Task(
                5, "Task 5", "", False, "2025-12-04T10:01:00.000000Z", "2025-12-04T10:01:00.000000Z"
            ),
            Task(
                3, "Task 3", "", False, "2025-12-04T10:02:00.000000Z", "2025-12-04T10:02:00.000000Z"
            ),
        ]
        task_service._task_storage.extend(tasks)

        next_id = task_service.generate_next_id()
        assert next_id == 6


class TestCreateTask:
    """Tests for create_task() function."""

    def test_create_task_with_title_and_description(self):
        """Create task with valid title and description."""
        task = task_service.create_task("Buy groceries", "Milk and eggs")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.description == "Milk and eggs"
        assert task.completed is False
        assert task.created_at is not None
        assert task.updated_at is not None

    def test_create_task_with_empty_description(self):
        """Create task with valid title and empty description."""
        task = task_service.create_task("Buy milk", "")

        assert task.id == 1
        assert task.title == "Buy milk"
        assert task.description == ""
        assert task.completed is False

    def test_create_task_sequential_ids(self):
        """Multiple tasks get sequential IDs (1, 2, 3, ...)."""
        task1 = task_service.create_task("Task 1", "")
        task2 = task_service.create_task("Task 2", "")
        task3 = task_service.create_task("Task 3", "")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_create_task_sets_completed_false(self):
        """New task has completed=False."""
        task = task_service.create_task("Test", "")
        assert task.completed is False

    def test_create_task_generates_timestamps(self):
        """Task has valid created_at and updated_at timestamps."""
        task = task_service.create_task("Test", "")

        assert task.created_at is not None
        assert task.updated_at is not None
        assert len(task.created_at) > 0
        assert len(task.updated_at) > 0

    def test_create_task_timestamps_equal(self):
        """created_at equals updated_at for new tasks."""
        task = task_service.create_task("Test", "")
        assert task.created_at == task.updated_at

    def test_create_task_appends_to_storage(self):
        """Task is appended to _task_storage."""
        assert len(task_service._task_storage) == 0

        task = task_service.create_task("Test", "")

        assert len(task_service._task_storage) == 1
        assert task_service._task_storage[0] == task

    def test_create_task_returns_task_instance(self):
        """create_task() returns Task instance."""
        task = task_service.create_task("Test", "")
        assert isinstance(task, Task)


class TestGetAllTasks:
    """Tests for get_all_tasks() function."""

    def test_get_all_tasks_empty(self):
        """Returns empty list when no tasks exist."""
        tasks = task_service.get_all_tasks()
        assert tasks == []

    def test_get_all_tasks_returns_copy(self):
        """Returns a copy of storage, not the original list."""
        task_service.create_task("Test", "")
        tasks = task_service.get_all_tasks()

        # Modifying returned list shouldn't affect storage
        tasks.append(
            Task(
                99, "Fake", "", False, "2025-12-04T10:00:00.000000Z", "2025-12-04T10:00:00.000000Z"
            )
        )

        assert len(task_service._task_storage) == 1
        assert len(tasks) == 2

    def test_get_all_tasks_multiple(self):
        """Returns all tasks from storage."""
        task1 = task_service.create_task("Task 1", "")
        task2 = task_service.create_task("Task 2", "")

        tasks = task_service.get_all_tasks()

        assert len(tasks) == 2
        assert task1 in tasks
        assert task2 in tasks
