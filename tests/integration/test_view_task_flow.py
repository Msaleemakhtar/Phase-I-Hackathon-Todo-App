"""Integration tests for View Task feature end-to-end flows."""

from unittest.mock import patch

import pytest

from src.services import task_service


@pytest.fixture(autouse=True)
def reset_task_storage():
    """Reset task storage before each test."""
    task_service._task_storage.clear()
    yield
    task_service._task_storage.clear()


class TestViewTasksFlow:
    """End-to-end integration tests for View All Tasks feature."""

    def test_view_tasks_empty_list(self, capsys):
        """View tasks when no tasks exist shows 'No tasks found.' message."""
        from src.ui.prompts import display_task_list

        tasks = task_service.get_all_tasks()
        display_task_list(tasks)

        captured = capsys.readouterr()
        assert "No tasks found." in captured.out

    def test_view_tasks_single_task(self, capsys):
        """View tasks with one task displays correctly."""
        from src.ui.prompts import display_task_list

        task_service.create_task("Buy groceries", "Milk and eggs")

        tasks = task_service.get_all_tasks()
        display_task_list(tasks)

        captured = capsys.readouterr()
        assert "1. [ ] Buy groceries" in captured.out
        assert "Total: 1 task" in captured.out

    def test_view_tasks_multiple_tasks(self, capsys):
        """View tasks with multiple tasks displays all in order."""
        from src.ui.prompts import display_task_list

        task_service.create_task("Task 1", "Description 1")
        task_service.create_task("Task 2", "Description 2")
        task_service.create_task("Task 3", "Description 3")

        tasks = task_service.get_all_tasks()
        display_task_list(tasks)

        captured = capsys.readouterr()
        assert "1. [ ] Task 1" in captured.out
        assert "2. [ ] Task 2" in captured.out
        assert "3. [ ] Task 3" in captured.out
        assert "Total: 3 tasks" in captured.out

    @patch("builtins.input", return_value="")
    def test_view_tasks_pagination_flow(self, mock_input, capsys):
        """View tasks with 25 tasks triggers pagination."""
        from src.ui.prompts import display_task_list

        # Create 25 tasks
        for i in range(1, 26):
            task_service.create_task(f"Task {i}", f"Description {i}")

        tasks = task_service.get_all_tasks()
        display_task_list(tasks)

        captured = capsys.readouterr()
        assert "1. [ ] Task 1" in captured.out
        assert "20. [ ] Task 20" in captured.out
        assert "21. [ ] Task 21" in captured.out
        assert "25. [ ] Task 25" in captured.out
        assert "Total: 25 tasks" in captured.out
        # Pagination prompt should appear once (after 20th task)
        assert mock_input.call_count == 1


class TestViewTaskDetailsFlow:
    """End-to-end integration tests for View Task Details feature."""

    def test_view_task_details_valid_id(self, capsys):
        """View task details for existing task shows all fields."""
        from src.services.task_service import get_task_by_id
        from src.ui.prompts import display_task_details

        task_service.create_task("Buy groceries", "Milk and eggs")

        task = get_task_by_id(1)
        display_task_details(task)

        captured = capsys.readouterr()
        assert "ID: 1" in captured.out
        assert "Title: Buy groceries" in captured.out
        assert "Description: Milk and eggs" in captured.out
        assert "Completed: No" in captured.out
        assert "Created At:" in captured.out
        assert "Updated At:" in captured.out

    def test_view_task_details_empty_description(self, capsys):
        """View task details for task with empty description shows placeholder."""
        from src.services.task_service import get_task_by_id
        from src.ui.prompts import display_task_details

        task_service.create_task("Call dentist", "")

        task = get_task_by_id(1)
        display_task_details(task)

        captured = capsys.readouterr()
        assert "Description: (No description)" in captured.out

    def test_view_task_details_invalid_id_not_found(self):
        """View task details for non-existent ID raises ERROR 101."""
        from src.services.task_service import get_task_by_id

        task_service.create_task("Task 1", "")
        task_service.create_task("Task 2", "")

        with pytest.raises(ValueError) as exc_info:
            get_task_by_id(99)

        assert "ERROR 101" in str(exc_info.value)
        assert "Task with ID 99 not found" in str(exc_info.value)

    def test_view_task_details_invalid_id_zero(self):
        """View task details for ID 0 raises ERROR 103."""
        from src.services.task_service import get_task_by_id

        with pytest.raises(ValueError) as exc_info:
            get_task_by_id(0)

        assert "ERROR 103" in str(exc_info.value)
        assert "positive number" in str(exc_info.value)

    def test_view_task_details_invalid_id_negative(self):
        """View task details for negative ID raises ERROR 103."""
        from src.services.task_service import get_task_by_id

        with pytest.raises(ValueError) as exc_info:
            get_task_by_id(-5)

        assert "ERROR 103" in str(exc_info.value)

    def test_view_task_details_with_prompt_validation(self, monkeypatch):
        """End-to-end: Prompt for task ID with valid input returns task ID."""
        from src.ui.prompts import prompt_for_task_id

        monkeypatch.setattr("builtins.input", lambda _: "5")

        task_id = prompt_for_task_id()
        assert task_id == 5

    def test_view_task_details_with_prompt_non_numeric(self, monkeypatch):
        """End-to-end: Prompt for task ID with non-numeric input raises ERROR 102."""
        from src.ui.prompts import prompt_for_task_id

        monkeypatch.setattr("builtins.input", lambda _: "abc")

        with pytest.raises(ValueError) as exc_info:
            prompt_for_task_id()

        assert "ERROR 102" in str(exc_info.value)


class TestViewTasksCompleteFlow:
    """Complete end-to-end scenarios from spec acceptance criteria."""

    def test_acceptance_scenario_1_three_tasks(self, capsys):
        """Given 3 tasks exist, when user views tasks, then all 3 display with indicators and count."""
        from src.ui.prompts import display_task_list

        # Given: 3 tasks exist
        task_service.create_task("Buy groceries", "")
        task_service.create_task("Complete project report", "")
        task_service.create_task("Call dentist", "")

        # Simulate marking task 2 as completed
        task_service._task_storage[1].completed = True

        # When: User selects "View Tasks"
        tasks = task_service.get_all_tasks()
        display_task_list(tasks)

        # Then: All 3 tasks display with ID, completion indicator, title, and count summary
        captured = capsys.readouterr()
        assert "1. [ ] Buy groceries" in captured.out
        assert "2. [X] Complete project report" in captured.out
        assert "3. [ ] Call dentist" in captured.out
        assert "Total: 3 tasks" in captured.out

    def test_acceptance_scenario_2_empty_list(self, capsys):
        """Given task list is empty, when user views tasks, then 'No tasks found.' is displayed."""
        from src.ui.prompts import display_task_list

        # Given: Task list is empty (reset_task_storage fixture handles this)

        # When: User selects "View Tasks"
        tasks = task_service.get_all_tasks()
        display_task_list(tasks)

        # Then: System displays "No tasks found."
        captured = capsys.readouterr()
        assert "No tasks found." in captured.out

    def test_acceptance_scenario_3_task_details_with_description(self, capsys):
        """Given task with ID 2 exists, when user enters ID 2, then all fields display with labels."""
        from src.services.task_service import get_task_by_id
        from src.ui.prompts import display_task_details

        # Given: Task with ID 2 exists with all fields populated
        task_service.create_task("Task 1", "")
        task_service.create_task("Buy groceries", "Milk, eggs, bread")

        # When: User enters ID "2"
        task = get_task_by_id(2)
        display_task_details(task)

        # Then: All fields display with labels
        captured = capsys.readouterr()
        assert "ID: 2" in captured.out
        assert "Title: Buy groceries" in captured.out
        assert "Description: Milk, eggs, bread" in captured.out
        assert "Completed: No" in captured.out
        assert "Created At:" in captured.out
        assert "Updated At:" in captured.out

    def test_acceptance_scenario_4_empty_description_placeholder(self, capsys):
        """Given task has empty description, when user views details, then '(No description)' is shown."""
        from src.services.task_service import get_task_by_id
        from src.ui.prompts import display_task_details

        # Given: Task with empty description
        task_service.create_task("Call dentist", "")

        # When: User views details
        task = get_task_by_id(1)
        display_task_details(task)

        # Then: Description shows "(No description)"
        captured = capsys.readouterr()
        assert "Description: (No description)" in captured.out
