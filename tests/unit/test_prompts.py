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


class TestDisplayFieldSelectionMenu:
    """Tests for display_field_selection_menu() function."""

    def test_display_field_selection_menu_output(self, capsys):
        """Test field selection menu displays correct format."""
        from src.ui.prompts import display_field_selection_menu

        display_field_selection_menu()

        captured = capsys.readouterr()
        assert "Select fields to update:" in captured.out
        assert "1. Update Title Only" in captured.out
        assert "2. Update Description Only" in captured.out
        assert "3. Update Both Title and Description" in captured.out


class TestPromptForFieldChoice:
    """Tests for prompt_for_field_choice() function."""

    def test_prompt_for_field_choice_valid_option_1(self, monkeypatch):
        """Accept choice 1 (Title Only)."""
        from src.ui.prompts import prompt_for_field_choice

        inputs = iter(["1"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        choice = prompt_for_field_choice()
        assert choice == 1

    def test_prompt_for_field_choice_valid_option_2(self, monkeypatch):
        """Accept choice 2 (Description Only)."""
        from src.ui.prompts import prompt_for_field_choice

        inputs = iter(["2"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        choice = prompt_for_field_choice()
        assert choice == 2

    def test_prompt_for_field_choice_valid_option_3(self, monkeypatch):
        """Accept choice 3 (Both)."""
        from src.ui.prompts import prompt_for_field_choice

        inputs = iter(["3"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        choice = prompt_for_field_choice()
        assert choice == 3

    def test_prompt_for_field_choice_invalid_option_reprompts(self, monkeypatch, capsys):
        """Display ERROR 104 for invalid numeric option and re-prompt."""
        from src.ui.prompts import prompt_for_field_choice

        inputs = iter(["4", "1"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        choice = prompt_for_field_choice()

        captured = capsys.readouterr()
        assert "ERROR 104" in captured.out
        assert choice == 1

    def test_prompt_for_field_choice_zero_reprompts(self, monkeypatch, capsys):
        """Display ERROR 104 for zero and re-prompt."""
        from src.ui.prompts import prompt_for_field_choice

        inputs = iter(["0", "2"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        choice = prompt_for_field_choice()

        captured = capsys.readouterr()
        assert "ERROR 104" in captured.out
        assert choice == 2

    def test_prompt_for_field_choice_non_numeric_reprompts(self, monkeypatch, capsys):
        """Display ERROR 104 for non-numeric input and re-prompt."""
        from src.ui.prompts import prompt_for_field_choice

        inputs = iter(["abc", "3"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        choice = prompt_for_field_choice()

        captured = capsys.readouterr()
        assert "ERROR 104" in captured.out
        assert choice == 3


class TestGetNewTaskTitle:
    """Tests for get_new_task_title() function."""

    def test_get_new_task_title_valid(self, monkeypatch):
        """Accept valid new title."""
        from src.ui.prompts import get_new_task_title

        inputs = iter(["Updated Title"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        title = get_new_task_title("Original Title")
        assert title == "Updated Title"

    def test_get_new_task_title_strips_whitespace(self, monkeypatch):
        """Strip leading/trailing whitespace from title."""
        from src.ui.prompts import get_new_task_title

        inputs = iter(["  Updated Title  "])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        title = get_new_task_title("Original")
        assert title == "Updated Title"

    def test_get_new_task_title_empty_reprompts(self, monkeypatch, capsys):
        """Display ERROR 001 for empty title and re-prompt."""
        from src.ui.prompts import get_new_task_title

        inputs = iter(["", "Valid Title"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        title = get_new_task_title("Original")

        captured = capsys.readouterr()
        assert "ERROR 001" in captured.out
        assert title == "Valid Title"

    def test_get_new_task_title_whitespace_only_reprompts(self, monkeypatch, capsys):
        """Display ERROR 001 for whitespace-only title and re-prompt."""
        from src.ui.prompts import get_new_task_title

        inputs = iter(["   ", "Valid Title"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        title = get_new_task_title("Original")

        captured = capsys.readouterr()
        assert "ERROR 001" in captured.out
        assert title == "Valid Title"

    def test_get_new_task_title_too_long_reprompts(self, monkeypatch, capsys):
        """Display ERROR 002 for title > 200 chars and re-prompt."""
        from src.ui.prompts import get_new_task_title

        long_title = "A" * 201
        inputs = iter([long_title, "Valid Title"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        title = get_new_task_title("Original")

        captured = capsys.readouterr()
        assert "ERROR 002" in captured.out
        assert title == "Valid Title"

    def test_get_new_task_title_exactly_200_chars_valid(self, monkeypatch):
        """Accept title with exactly 200 characters."""
        from src.ui.prompts import get_new_task_title

        exact_title = "A" * 200
        inputs = iter([exact_title])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        title = get_new_task_title("Original")
        assert title == exact_title


class TestGetNewTaskDescription:
    """Tests for get_new_task_description() function."""

    def test_get_new_task_description_valid(self, monkeypatch):
        """Accept valid new description."""
        from src.ui.prompts import get_new_task_description

        inputs = iter(["Updated Description"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        description = get_new_task_description("Original Description")
        assert description == "Updated Description"

    def test_get_new_task_description_empty_allowed(self, monkeypatch):
        """Allow empty description (valid)."""
        from src.ui.prompts import get_new_task_description

        inputs = iter([""])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        description = get_new_task_description("Original")
        assert description == ""

    def test_get_new_task_description_strips_whitespace(self, monkeypatch):
        """Strip leading/trailing whitespace from description."""
        from src.ui.prompts import get_new_task_description

        inputs = iter(["  Updated Description  "])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        description = get_new_task_description("Original")
        assert description == "Updated Description"

    def test_get_new_task_description_too_long_reprompts(self, monkeypatch, capsys):
        """Display ERROR 003 for description > 1000 chars and re-prompt."""
        from src.ui.prompts import get_new_task_description

        long_desc = "A" * 1001
        inputs = iter([long_desc, "Valid Description"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        description = get_new_task_description("Original")

        captured = capsys.readouterr()
        assert "ERROR 003" in captured.out
        assert description == "Valid Description"

    def test_get_new_task_description_exactly_1000_chars_valid(self, monkeypatch):
        """Accept description with exactly 1000 characters."""
        from src.ui.prompts import get_new_task_description

        exact_desc = "A" * 1000
        inputs = iter([exact_desc])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        description = get_new_task_description("Original")
        assert description == exact_desc


class TestUpdateTaskPrompt:
    """Tests for update_task_prompt() orchestrator function."""

    @pytest.fixture(autouse=True)
    def setup_storage(self):
        """Reset task storage before each test."""
        from src.services import task_service

        task_service._task_storage.clear()
        task_service.create_task("Original Title", "Original Description")
        yield
        task_service._task_storage.clear()

    def test_update_task_prompt_option_1_title_only(self, monkeypatch, capsys):
        """Test complete flow for option 1 (title only)."""
        from src.services import task_service
        from src.ui.prompts import update_task_prompt

        inputs = iter(["1", "1", "Updated Title"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        update_task_prompt()

        task = task_service.get_task_by_id(1)
        assert task.title == "Updated Title"
        assert task.description == "Original Description"

        captured = capsys.readouterr()
        assert "Task updated successfully." in captured.out

    def test_update_task_prompt_option_2_description_only(self, monkeypatch, capsys):
        """Test complete flow for option 2 (description only)."""
        from src.services import task_service
        from src.ui.prompts import update_task_prompt

        inputs = iter(["1", "2", "Updated Description"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        update_task_prompt()

        task = task_service.get_task_by_id(1)
        assert task.title == "Original Title"
        assert task.description == "Updated Description"

        captured = capsys.readouterr()
        assert "Task updated successfully." in captured.out

    def test_update_task_prompt_option_3_both_fields(self, monkeypatch, capsys):
        """Test complete flow for option 3 (both fields)."""
        from src.services import task_service
        from src.ui.prompts import update_task_prompt

        inputs = iter(["1", "3", "Updated Title", "Updated Description"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        update_task_prompt()

        task = task_service.get_task_by_id(1)
        assert task.title == "Updated Title"
        assert task.description == "Updated Description"

        captured = capsys.readouterr()
        assert "Task updated successfully." in captured.out

    def test_update_task_prompt_task_not_found(self, monkeypatch, capsys):
        """Test ERROR 101 displayed when task doesn't exist."""
        from src.ui.prompts import update_task_prompt

        inputs = iter(["99"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        update_task_prompt()

        captured = capsys.readouterr()
        assert "ERROR 101" in captured.out

    def test_update_task_prompt_invalid_task_id_zero(self, monkeypatch, capsys):
        """Test ERROR 103 displayed for task_id = 0."""
        from src.ui.prompts import update_task_prompt

        inputs = iter(["0"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        update_task_prompt()

        captured = capsys.readouterr()
        assert "ERROR 103" in captured.out

    def test_update_task_prompt_invalid_task_id_negative(self, monkeypatch, capsys):
        """Test ERROR 103 displayed for negative task_id."""
        from src.ui.prompts import update_task_prompt

        inputs = iter(["-1"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        update_task_prompt()

        captured = capsys.readouterr()
        assert "ERROR 103" in captured.out

    def test_update_task_prompt_invalid_task_id_non_numeric(self, monkeypatch, capsys):
        """Test ERROR 102 displayed for non-numeric task_id."""
        from src.ui.prompts import update_task_prompt

        inputs = iter(["abc"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        update_task_prompt()

        captured = capsys.readouterr()
        assert "ERROR 102" in captured.out

    def test_update_task_prompt_displays_current_values(self, monkeypatch, capsys):
        """Test that current task values are displayed before update."""
        from src.ui.prompts import update_task_prompt

        inputs = iter(["1", "1", "Updated"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        update_task_prompt()

        captured = capsys.readouterr()
        assert "Original Title" in captured.out
        assert "Original Description" in captured.out

    def test_update_task_prompt_title_unchanged_when_option_2(self, monkeypatch):
        """Verify title unchanged when option 2 (description only) selected."""
        from src.services import task_service
        from src.ui.prompts import update_task_prompt

        inputs = iter(["1", "2", "New Description"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        update_task_prompt()

        task = task_service.get_task_by_id(1)
        assert task.title == "Original Title"

    def test_update_task_prompt_description_unchanged_when_option_1(self, monkeypatch):
        """Verify description unchanged when option 1 (title only) selected."""
        from src.services import task_service
        from src.ui.prompts import update_task_prompt

        inputs = iter(["1", "1", "New Title"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        update_task_prompt()

        task = task_service.get_task_by_id(1)
        assert task.description == "Original Description"


class TestPromptForDeleteConfirmation:
    """Tests for prompt_for_delete_confirmation() function."""

    def test_confirm_with_uppercase_y(self, monkeypatch):
        """Input 'Y' returns True."""
        from src.ui.prompts import prompt_for_delete_confirmation

        monkeypatch.setattr("builtins.input", lambda _: "Y")

        result = prompt_for_delete_confirmation("Test Task")

        assert result is True

    def test_confirm_with_lowercase_y(self, monkeypatch):
        """Input 'y' returns True."""
        from src.ui.prompts import prompt_for_delete_confirmation

        monkeypatch.setattr("builtins.input", lambda _: "y")

        result = prompt_for_delete_confirmation("Test Task")

        assert result is True

    def test_cancel_with_uppercase_n(self, monkeypatch):
        """Input 'N' returns False."""
        from src.ui.prompts import prompt_for_delete_confirmation

        monkeypatch.setattr("builtins.input", lambda _: "N")

        result = prompt_for_delete_confirmation("Test Task")

        assert result is False

    def test_cancel_with_lowercase_n(self, monkeypatch):
        """Input 'n' returns False."""
        from src.ui.prompts import prompt_for_delete_confirmation

        monkeypatch.setattr("builtins.input", lambda _: "n")

        result = prompt_for_delete_confirmation("Test Task")

        assert result is False

    def test_strips_whitespace(self, monkeypatch):
        """Input ' Y ' (with spaces) returns True."""
        from src.ui.prompts import prompt_for_delete_confirmation

        monkeypatch.setattr("builtins.input", lambda _: " Y ")

        result = prompt_for_delete_confirmation("Test Task")

        assert result is True

    def test_invalid_then_valid_response(self, monkeypatch, capsys):
        """Invalid input shows ERROR 105, then re-prompts."""
        from src.ui.prompts import prompt_for_delete_confirmation

        inputs = iter(["maybe", "Y"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        result = prompt_for_delete_confirmation("Test Task")

        assert result is True

        # Verify ERROR 105 was printed
        captured = capsys.readouterr()
        assert "ERROR 105" in captured.out
