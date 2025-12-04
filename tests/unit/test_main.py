"""Unit tests for main application menu."""

from unittest.mock import call, patch

import pytest

from src.main import handle_add_task, main


class TestHandleAddTask:
    """Tests for handle_add_task function."""

    @patch("src.main.print")
    @patch("src.main.create_task")
    @patch("src.main.get_task_description")
    @patch("src.main.get_task_title")
    def test_handle_add_task_full_flow(
        self, mock_get_title, mock_get_desc, mock_create, mock_print
    ):
        """Test complete add task flow with mocked inputs."""
        mock_get_title.return_value = "Test Task"
        mock_get_desc.return_value = "Test Description"

        handle_add_task()

        mock_get_title.assert_called_once()
        mock_get_desc.assert_called_once()
        mock_create.assert_called_once_with("Test Task", "Test Description")
        mock_print.assert_called_once_with("Task added successfully.")


class TestMainMenu:
    """Tests for main menu loop."""

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.main.handle_add_task")
    def test_main_menu_option_1_add_task(self, mock_handle, mock_print, mock_input):
        """Test selecting option 1 calls handle_add_task."""
        mock_input.side_effect = ["1", "6"]  # Select Add Task, then Exit

        main()

        mock_handle.assert_called_once()
        assert any("Goodbye!" in str(call) for call in mock_print.call_args_list)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_menu_option_6_exit(self, mock_print, mock_input):
        """Test selecting option 6 exits with goodbye message."""
        mock_input.return_value = "6"

        main()

        assert any("Goodbye!" in str(call) for call in mock_print.call_args_list)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_menu_invalid_option(self, mock_print, mock_input):
        """Test invalid option shows error message."""
        mock_input.side_effect = ["99", "6"]  # Invalid option, then Exit

        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any(
            "Feature not yet implemented or invalid option." in call for call in print_calls
        )

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_menu_future_features(self, mock_print, mock_input):
        """Test future feature options show not implemented message."""
        # Test options 2, 3, 4, 5 (all future features)
        mock_input.side_effect = ["2", "3", "4", "5", "6"]

        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        # Should see "not implemented" message 4 times (for options 2, 3, 4, 5)
        not_implemented_count = sum(
            1 for call in print_calls if "Feature not yet implemented" in call
        )
        assert not_implemented_count == 4

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_menu_displays_all_options(self, mock_print, mock_input):
        """Test main menu displays all 6 options."""
        mock_input.return_value = "6"

        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("=== Todo App ===" in call for call in print_calls)
        assert any("1. Add Task" in call for call in print_calls)
        assert any("2. View Tasks" in call for call in print_calls)
        assert any("3. Update Task" in call for call in print_calls)
        assert any("4. Delete Task" in call for call in print_calls)
        assert any("5. Mark Complete" in call for call in print_calls)
        assert any("6. Exit" in call for call in print_calls)

    @patch("builtins.input")
    @patch("builtins.print")
    @patch("src.main.handle_add_task")
    def test_main_menu_multiple_operations(self, mock_handle, mock_print, mock_input):
        """Test multiple operations in sequence."""
        # Add task twice, try invalid option, then exit
        mock_input.side_effect = ["1", "1", "invalid", "6"]

        main()

        assert mock_handle.call_count == 2
        assert any("Goodbye!" in str(call) for call in mock_print.call_args_list)

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_menu_empty_input(self, mock_print, mock_input):
        """Test empty input treated as invalid option."""
        mock_input.side_effect = ["", "6"]

        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any(
            "Feature not yet implemented or invalid option." in call for call in print_calls
        )

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_menu_whitespace_input(self, mock_print, mock_input):
        """Test whitespace input treated as invalid option."""
        mock_input.side_effect = ["   ", "6"]

        main()

        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any(
            "Feature not yet implemented or invalid option." in call for call in print_calls
        )

    @patch("builtins.input")
    @patch("builtins.print")
    def test_main_menu_loop_continues_after_operation(self, mock_print, mock_input):
        """Test menu loop continues after each operation."""
        mock_input.side_effect = ["2", "3", "6"]  # View, Update, Exit

        main()

        # Should see menu displayed 3 times (once for each iteration)
        menu_count = sum(1 for call in mock_print.call_args_list if "=== Todo App ===" in str(call))
        assert menu_count == 3
