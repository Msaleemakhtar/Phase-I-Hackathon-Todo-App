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


class TestGetTaskById:
    """Tests for get_task_by_id() function."""

    def test_get_task_by_id_exists(self):
        """Returns task with matching ID."""
        task = task_service.create_task("Test Task", "Description")
        retrieved = task_service.get_task_by_id(1)

        assert retrieved == task
        assert retrieved.id == 1

    def test_get_task_by_id_nonexistent(self):
        """Raises ValueError when task doesn't exist (ERROR 101)."""
        task_service.create_task("Test", "")

        with pytest.raises(ValueError, match="ERROR 101"):
            task_service.get_task_by_id(99)

    def test_get_task_by_id_zero(self):
        """Raises ValueError for task_id = 0 (ERROR 103)."""
        with pytest.raises(ValueError, match="ERROR 103"):
            task_service.get_task_by_id(0)

    def test_get_task_by_id_negative(self):
        """Raises ValueError for negative task_id (ERROR 103)."""
        with pytest.raises(ValueError, match="ERROR 103"):
            task_service.get_task_by_id(-1)


class TestUpdateTask:
    """Tests for update_task() function."""

    def test_update_task_title_only(self):
        """Test updating only the title field."""
        task = task_service.create_task("Original Title", "Original Description")
        original_description = task.description
        original_id = task.id
        original_created_at = task.created_at

        updated = task_service.update_task(1, new_title="Updated Title")

        assert updated.title == "Updated Title"
        assert updated.description == original_description
        assert updated.id == original_id
        assert updated.created_at == original_created_at

    def test_update_task_description_only(self):
        """Test updating only the description field."""
        task = task_service.create_task("Original Title", "Original Description")
        original_title = task.title
        original_id = task.id
        original_created_at = task.created_at

        updated = task_service.update_task(1, new_description="Updated Description")

        assert updated.title == original_title
        assert updated.description == "Updated Description"
        assert updated.id == original_id
        assert updated.created_at == original_created_at

    def test_update_task_both_fields(self):
        """Test updating both title and description."""
        task = task_service.create_task("Original Title", "Original Description")
        original_id = task.id
        original_created_at = task.created_at

        updated = task_service.update_task(
            1, new_title="Updated Title", new_description="Updated Description"
        )

        assert updated.title == "Updated Title"
        assert updated.description == "Updated Description"
        assert updated.id == original_id
        assert updated.created_at == original_created_at

    def test_update_task_updates_timestamp(self):
        """Test that updated_at timestamp changes on update."""
        import time

        task = task_service.create_task("Test", "Description")
        original_updated_at = task.updated_at

        # Small delay to ensure timestamp difference
        time.sleep(0.01)

        updated = task_service.update_task(1, new_title="Updated")

        assert updated.updated_at != original_updated_at

    def test_update_task_preserves_immutable_fields(self):
        """Test that id, completed, created_at are not modified."""
        task = task_service.create_task("Test", "Description")
        original_id = task.id
        original_completed = task.completed
        original_created_at = task.created_at

        task_service.update_task(1, new_title="Updated", new_description="Updated Desc")

        assert task.id == original_id
        assert task.completed == original_completed
        assert task.created_at == original_created_at

    def test_update_task_invalid_id_zero(self):
        """Test updating with task_id = 0 raises ERROR 103."""
        task_service.create_task("Test", "")

        with pytest.raises(ValueError, match="ERROR 103"):
            task_service.update_task(0, new_title="Updated")

    def test_update_task_invalid_id_negative(self):
        """Test updating with task_id = -1 raises ERROR 103."""
        task_service.create_task("Test", "")

        with pytest.raises(ValueError, match="ERROR 103"):
            task_service.update_task(-1, new_title="Updated")

    def test_update_task_nonexistent_id(self):
        """Test updating non-existent task raises ERROR 101."""
        task_service.create_task("Test", "")

        with pytest.raises(ValueError, match="ERROR 101"):
            task_service.update_task(99, new_title="Updated")

    def test_update_task_returns_same_instance(self):
        """Test that update returns the same Task object (in-place modification)."""
        task = task_service.create_task("Test", "Description")
        updated = task_service.update_task(1, new_title="Updated")

        assert updated is task

    def test_update_task_with_none_values(self):
        """Test calling update_task with both new_title=None, new_description=None."""
        task = task_service.create_task("Original", "Description")
        original_title = task.title
        original_description = task.description
        original_updated_at = task.updated_at

        import time

        time.sleep(0.01)

        updated = task_service.update_task(1)

        # Fields should be unchanged
        assert updated.title == original_title
        assert updated.description == original_description
        # But timestamp should update
        assert updated.updated_at != original_updated_at
