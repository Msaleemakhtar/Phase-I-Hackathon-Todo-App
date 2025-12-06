"""Unit tests for UI prompts and display functions."""

from unittest.mock import patch

import pytest

from src.models.task import Task


class TestDisplayTaskList:
    """Tests for display_task_list() function."""

    def test_display_task_list_empty(self, capsys):
        """Display 'No tasks found.' message for empty list."""
        from src.ui.prompts import display_task_list

        display_task_list([])

        captured = capsys.readouterr()
        assert "No tasks found." in captured.out

    def test_display_task_list_single_incomplete_task(self, capsys):
        """Display single incomplete task with [ ] indicator."""
        from src.ui.prompts import display_task_list

        task = Task(
            id=1,
            title="Buy groceries",
            description="Milk and eggs",
            completed=False,
            created_at="2025-12-06T10:00:00.000000Z",
            updated_at="2025-12-06T10:00:00.000000Z",
        )

        display_task_list([task])

        captured = capsys.readouterr()
        assert "1. [ ] Buy groceries" in captured.out
        assert "Total: 1 task" in captured.out

    def test_display_task_list_single_completed_task(self, capsys):
        """Display single completed task with [X] indicator."""
        from src.ui.prompts import display_task_list

        task = Task(
            id=2,
            title="Complete project",
            description="",
            completed=True,
            created_at="2025-12-06T10:00:00.000000Z",
            updated_at="2025-12-06T10:00:00.000000Z",
        )

        display_task_list([task])

        captured = capsys.readouterr()
        assert "2. [X] Complete project" in captured.out
        assert "Total: 1 task" in captured.out

    def test_display_task_list_multiple_tasks(self, capsys):
        """Display multiple tasks with correct indicators."""
        from src.ui.prompts import display_task_list

        tasks = [
            Task(
                1, "Task 1", "", False, "2025-12-06T10:00:00.000000Z", "2025-12-06T10:00:00.000000Z"
            ),
            Task(
                2, "Task 2", "", True, "2025-12-06T10:01:00.000000Z", "2025-12-06T10:01:00.000000Z"
            ),
            Task(
                3, "Task 3", "", False, "2025-12-06T10:02:00.000000Z", "2025-12-06T10:02:00.000000Z"
            ),
        ]

        display_task_list(tasks)

        captured = capsys.readouterr()
        assert "1. [ ] Task 1" in captured.out
        assert "2. [X] Task 2" in captured.out
        assert "3. [ ] Task 3" in captured.out
        assert "Total: 3 tasks" in captured.out

    def test_display_task_list_total_count_plural(self, capsys):
        """Display 'tasks' (plural) for count > 1."""
        from src.ui.prompts import display_task_list

        tasks = [
            Task(
                1, "Task 1", "", False, "2025-12-06T10:00:00.000000Z", "2025-12-06T10:00:00.000000Z"
            ),
            Task(
                2, "Task 2", "", False, "2025-12-06T10:01:00.000000Z", "2025-12-06T10:01:00.000000Z"
            ),
        ]

        display_task_list(tasks)

        captured = capsys.readouterr()
        assert "Total: 2 tasks" in captured.out

    def test_display_task_list_no_pagination_at_20(self, capsys, monkeypatch):
        """No pagination prompt when exactly 20 tasks."""
        from src.ui.prompts import display_task_list

        # Create 20 tasks
        tasks = [
            Task(
                i,
                f"Task {i}",
                "",
                False,
                "2025-12-06T10:00:00.000000Z",
                "2025-12-06T10:00:00.000000Z",
            )
            for i in range(1, 21)
        ]

        # Mock input to detect if it was called
        input_called = []
        monkeypatch.setattr("builtins.input", lambda x: input_called.append(x) or "")

        display_task_list(tasks)

        captured = capsys.readouterr()
        assert "Total: 20 tasks" in captured.out
        assert len(input_called) == 0, "Pagination prompt should not appear for exactly 20 tasks"

    @patch("builtins.input", return_value="")
    def test_display_task_list_pagination_at_21(self, mock_input, capsys):
        """Pagination prompt appears when 21 tasks."""
        from src.ui.prompts import display_task_list

        # Create 21 tasks
        tasks = [
            Task(
                i,
                f"Task {i}",
                "",
                False,
                "2025-12-06T10:00:00.000000Z",
                "2025-12-06T10:00:00.000000Z",
            )
            for i in range(1, 22)
        ]

        display_task_list(tasks)

        captured = capsys.readouterr()
        assert "Total: 21 tasks" in captured.out
        # Verify pagination prompt was called once
        assert mock_input.call_count == 1
        assert "Press Enter to continue..." in mock_input.call_args[0][0]

    @patch("builtins.input", return_value="")
    def test_display_task_list_pagination_at_40(self, mock_input, capsys):
        """Pagination prompt appears after 20 and 40 tasks."""
        from src.ui.prompts import display_task_list

        # Create 40 tasks
        tasks = [
            Task(
                i,
                f"Task {i}",
                "",
                False,
                "2025-12-06T10:00:00.000000Z",
                "2025-12-06T10:00:00.000000Z",
            )
            for i in range(1, 41)
        ]

        display_task_list(tasks)

        captured = capsys.readouterr()
        assert "Total: 40 tasks" in captured.out
        # Verify pagination prompt was called once (after 20th task)
        # No prompt after 40th because it's the last task
        assert mock_input.call_count == 1

    @patch("builtins.input", return_value="")
    def test_display_task_list_pagination_at_45(self, mock_input, capsys):
        """Pagination prompt appears twice for 45 tasks (after 20 and 40)."""
        from src.ui.prompts import display_task_list

        # Create 45 tasks
        tasks = [
            Task(
                i,
                f"Task {i}",
                "",
                False,
                "2025-12-06T10:00:00.000000Z",
                "2025-12-06T10:00:00.000000Z",
            )
            for i in range(1, 46)
        ]

        display_task_list(tasks)

        captured = capsys.readouterr()
        assert "Total: 45 tasks" in captured.out
        # Verify pagination prompt was called twice (after 20th and 40th)
        assert mock_input.call_count == 2

    def test_display_task_list_long_titles(self, capsys):
        """Display long titles without truncation."""
        from src.ui.prompts import display_task_list

        long_title = "A" * 200  # Maximum title length
        task = Task(
            1, long_title, "", False, "2025-12-06T10:00:00.000000Z", "2025-12-06T10:00:00.000000Z"
        )

        display_task_list([task])

        captured = capsys.readouterr()
        assert long_title in captured.out  # Full title should be displayed

    def test_display_task_list_special_characters(self, capsys):
        """Display special characters in titles as-is."""
        from src.ui.prompts import display_task_list

        task = Task(
            1,
            "Buy 🥛 and 🥚",
            "",
            False,
            "2025-12-06T10:00:00.000000Z",
            "2025-12-06T10:00:00.000000Z",
        )

        display_task_list([task])

        captured = capsys.readouterr()
        assert "Buy 🥛 and 🥚" in captured.out


class TestDisplayTaskDetails:
    """Tests for display_task_details() function."""

    def test_display_task_details_complete_task(self, capsys):
        """Display all fields for a completed task with description."""
        from src.ui.prompts import display_task_details

        task = Task(
            id=5,
            title="Buy groceries",
            description="Milk, eggs, bread",
            completed=True,
            created_at="2025-12-06T10:00:00.000000Z",
            updated_at="2025-12-06T11:30:00.000000Z",
        )

        display_task_details(task)

        captured = capsys.readouterr()
        assert "ID: 5" in captured.out
        assert "Title: Buy groceries" in captured.out
        assert "Description: Milk, eggs, bread" in captured.out
        assert "Completed: Yes" in captured.out
        assert "Created At: 2025-12-06T10:00:00.000000Z" in captured.out
        assert "Updated At: 2025-12-06T11:30:00.000000Z" in captured.out

    def test_display_task_details_incomplete_task(self, capsys):
        """Display 'No' for incomplete task."""
        from src.ui.prompts import display_task_details

        task = Task(
            2,
            "Task 2",
            "Description",
            False,
            "2025-12-06T10:00:00.000000Z",
            "2025-12-06T10:00:00.000000Z",
        )

        display_task_details(task)

        captured = capsys.readouterr()
        assert "Completed: No" in captured.out

    def test_display_task_details_empty_description(self, capsys):
        """Display '(No description)' for empty description."""
        from src.ui.prompts import display_task_details

        task = Task(
            3, "Task 3", "", False, "2025-12-06T10:00:00.000000Z", "2025-12-06T10:00:00.000000Z"
        )

        display_task_details(task)

        captured = capsys.readouterr()
        assert "Description: (No description)" in captured.out

    def test_display_task_details_whitespace_only_description(self, capsys):
        """Display '(No description)' for whitespace-only description."""
        from src.ui.prompts import display_task_details

        task = Task(
            4, "Task 4", "   ", False, "2025-12-06T10:00:00.000000Z", "2025-12-06T10:00:00.000000Z"
        )

        display_task_details(task)

        captured = capsys.readouterr()
        assert "Description: (No description)" in captured.out

    def test_display_task_details_multiline_description(self, capsys):
        """Display multiline description as-is."""
        from src.ui.prompts import display_task_details

        task = Task(
            6,
            "Shopping",
            "Items:\n- Milk\n- Eggs\n- Bread",
            False,
            "2025-12-06T10:00:00.000000Z",
            "2025-12-06T10:00:00.000000Z",
        )

        display_task_details(task)

        captured = capsys.readouterr()
        assert "Description: Items:\n- Milk\n- Eggs\n- Bread" in captured.out


class TestPromptForTaskId:
    """Tests for prompt_for_task_id() function."""

    def test_prompt_for_task_id_valid_positive(self, monkeypatch):
        """Return valid positive integer."""
        from src.ui.prompts import prompt_for_task_id

        monkeypatch.setattr("builtins.input", lambda _: "5")

        task_id = prompt_for_task_id()
        assert task_id == 5

    def test_prompt_for_task_id_invalid_non_numeric(self, monkeypatch):
        """Raise ERROR 102 for non-numeric input."""
        from src.ui.prompts import prompt_for_task_id

        inputs = iter(["abc"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError) as exc_info:
            prompt_for_task_id()

        assert "ERROR 102" in str(exc_info.value)
        assert "Invalid input" in str(exc_info.value)

    def test_prompt_for_task_id_invalid_zero(self, monkeypatch):
        """Raise ERROR 103 for zero."""
        from src.ui.prompts import prompt_for_task_id

        inputs = iter(["0"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError) as exc_info:
            prompt_for_task_id()

        assert "ERROR 103" in str(exc_info.value)
        assert "positive number" in str(exc_info.value)

    def test_prompt_for_task_id_invalid_negative(self, monkeypatch):
        """Raise ERROR 103 for negative number."""
        from src.ui.prompts import prompt_for_task_id

        inputs = iter(["-5"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError) as exc_info:
            prompt_for_task_id()

        assert "ERROR 103" in str(exc_info.value)

    def test_prompt_for_task_id_invalid_float(self, monkeypatch):
        """Raise ERROR 102 for float input."""
        from src.ui.prompts import prompt_for_task_id

        inputs = iter(["3.14"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError) as exc_info:
            prompt_for_task_id()

        assert "ERROR 102" in str(exc_info.value)

    def test_prompt_for_task_id_empty_string(self, monkeypatch):
        """Raise ERROR 102 for empty string."""
        from src.ui.prompts import prompt_for_task_id

        inputs = iter([""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(ValueError) as exc_info:
            prompt_for_task_id()

        assert "ERROR 102" in str(exc_info.value)
