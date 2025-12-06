"""
UI Layer Contract: View Task Feature

This file defines the public interface contract for display functions in ui/prompts.py.
These functions will be added to the existing prompts module.

Feature: 002-view-task
Date: 2025-12-06
Status: Design Contract
"""

from typing import Protocol

from src.models.task import Task


class ViewTaskUIProtocol(Protocol):
    """
    Protocol defining the contract for view display functions in ui/prompts.py.

    These functions handle all console output for the View Task feature.
    They do not perform validation or business logic - only formatting and display.
    """

    def display_task_list(self, tasks: list[Task]) -> None:
        """
        Display a formatted list of all tasks with completion indicators and pagination.

        Args:
            tasks (list[Task]): List of Task objects to display.
                               Can be empty (will display "No tasks found.").

        Returns:
            None: Outputs directly to console.

        Behavior:
            - If tasks is empty: Display "No tasks found." and return
            - For each task: Display "{id}. [{indicator}] {title}"
              where indicator is "[X]" if completed, "[ ]" if not
            - After every 20 tasks (if more tasks remain): Display "Press Enter to continue..."
              and wait for user input
            - After all tasks: Display "Total: {count} tasks"

        Format Specification:
            - Completion indicator: "[ ]" (incomplete) or "[X]" (complete)
            - Line format: "{id}. {indicator} {title}"
            - No truncation of titles (let terminal wrap)
            - Summary line: "Total: {count} tasks" (singular "task" if count == 1)

        Example Output (3 tasks):
            1. [ ] Buy groceries
            2. [X] Complete project report
            3. [ ] Call dentist

            Total: 3 tasks

        Example Output (pagination, 25 tasks):
            1. [ ] Task 1
            ...
            20. [ ] Task 20
            Press Enter to continue...
            21. [ ] Task 21
            ...
            25. [ ] Task 25

            Total: 25 tasks

        Example Output (empty list):
            No tasks found.

        Testing:
            - Test with empty list → displays "No tasks found."
            - Test with 1 task → no pagination, shows "Total: 1 task"
            - Test with 20 tasks → no pagination prompt
            - Test with 21 tasks → pagination prompt appears after task 20
            - Test with 40 tasks → pagination prompt appears after tasks 20
            - Test completed vs incomplete → correct indicators
            - Test long titles → natural wrapping (no truncation)

        Side Effects:
            - Writes to stdout (print statements)
            - Blocks on input() for pagination prompts
        """
        ...

    def display_task_details(self, task: Task) -> None:
        """
        Display detailed information for a single task with all fields labeled.

        Args:
            task (Task): The Task object to display in detail.

        Returns:
            None: Outputs directly to console.

        Behavior:
            - Display all 6 task fields with labels
            - Empty descriptions show "(No description)" placeholder
            - Completed field shows "Yes" or "No" (not True/False)
            - Timestamps displayed in ISO 8601 format as-is

        Format Specification:
            ID: {task.id}
            Title: {task.title}
            Description: {task.description or "(No description)"}
            Completed: {"Yes" if task.completed else "No"}
            Created At: {task.created_at}
            Updated At: {task.updated_at}

        Example Output (with description):
            ID: 2
            Title: Buy groceries
            Description: Milk, eggs, bread
            Completed: No
            Created At: 2025-12-06T10:00:00.000000Z
            Updated At: 2025-12-06T10:00:00.000000Z

        Example Output (empty description):
            ID: 5
            Title: Call dentist
            Description: (No description)
            Completed: Yes
            Created At: 2025-12-05T14:30:00.000000Z
            Updated At: 2025-12-06T09:15:00.000000Z

        Testing:
            - Test with complete task → "Completed: Yes"
            - Test with incomplete task → "Completed: No"
            - Test with empty description → "(No description)"
            - Test with whitespace-only description → "(No description)"
            - Test with multi-line description → preserves newlines
            - Test with special characters → displays as-is
            - Test with emojis → displays as-is

        Side Effects:
            - Writes to stdout (print statements)
        """
        ...

    def prompt_for_task_id(self) -> int:
        """
        Prompt user to enter a task ID and validate it's a positive integer.

        Returns:
            int: Valid positive task ID entered by user.

        Raises:
            ValueError: If input is non-numeric with message:
                       "ERROR 102: Invalid input. Please enter a numeric task ID."
            ValueError: If input is zero or negative with message:
                       "ERROR 103: Task ID must be a positive number."

        Behavior:
            - Display prompt: "Enter Task ID: "
            - Accept user input
            - Validate input is numeric (can convert to int)
            - Validate input is positive (> 0)
            - Return valid task_id or raise ValueError

        Error Handling:
            - Input "abc" → ValueError("ERROR 102: ...")
            - Input "12.5" → ValueError("ERROR 102: ...")
            - Input "" (empty) → ValueError("ERROR 102: ...")
            - Input "0" → ValueError("ERROR 103: ...")
            - Input "-5" → ValueError("ERROR 103: ...")
            - Input "42" → Returns 42

        Example:
            >>> try:
            ...     task_id = prompt_for_task_id()
            ...     print(f"Valid ID: {task_id}")
            ... except ValueError as e:
            ...     print(f"Error: {e}")
            Enter Task ID: abc
            Error: ERROR 102: Invalid input. Please enter a numeric task ID.

        Testing:
            - Test with valid positive int → returns int
            - Test with "0" → raises ERROR 103
            - Test with "-1" → raises ERROR 103
            - Test with "abc" → raises ERROR 102
            - Test with "3.14" → raises ERROR 102
            - Test with empty string → raises ERROR 102
            - Test error messages match exact format from spec

        Side Effects:
            - Writes to stdout (prompt)
            - Reads from stdin (input)
        """
        ...


# Contract Verification Notes:
# =============================
#
# 1. Separation of Concerns:
#    - Display functions only handle formatting and output
#    - Validation is minimal (only input type/range checking)
#    - Business logic (task existence) handled in service layer
#
# 2. Error Handling:
#    - ERROR 102: Non-numeric input (UI layer responsibility)
#    - ERROR 103: Invalid range (UI layer responsibility)
#    - ERROR 101: Task not found (service layer responsibility, caught by UI)
#
# 3. User Experience:
#    - Clear visual indicators ([ ] and [X])
#    - Labeled fields in detail view
#    - Pagination for large lists
#    - Helpful placeholder for empty descriptions
#
# 4. Display Formatting:
#    - No external libraries (no rich, colorama, etc.)
#    - Plain text output using print()
#    - Terminal handles text wrapping
#    - Preserves special characters as-is
#
# 5. Input Handling:
#    - Uses input() for user prompts
#    - Validates using try-except with int() conversion
#    - Re-raises ValueError with specific error codes
#
# 6. Pagination:
#    - Every 20 tasks in list view
#    - Uses simple counter (enumerate)
#    - Blocks on input("Press Enter to continue...")
#    - Only prompts if more tasks remain
#
# 7. Null Safety:
#    - display_task_list handles empty list gracefully
#    - display_task_details handles empty description
#    - No None checks needed (list is never None, description is empty string)
#
# 8. Testability:
#    - Functions can be tested with mock stdin/stdout
#    - pytest capsys fixture can capture output
#    - monkeypatch can provide mock input
