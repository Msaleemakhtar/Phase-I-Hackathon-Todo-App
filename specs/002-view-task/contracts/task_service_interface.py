"""
Service Layer Contract: View Task Feature

This file defines the public interface contract for view operations in TaskService.
These methods will be added to the existing TaskService class in src/services/task_service.py.

Feature: 002-view-task
Date: 2025-12-06
Status: Design Contract
"""

from typing import Protocol

from src.models.task import Task


class ViewTaskServiceProtocol(Protocol):
    """
    Protocol defining the contract for view operations in TaskService.

    This protocol extends the existing TaskService with read-only methods
    for retrieving tasks. Implementation must adhere to this contract.
    """

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieve all tasks in the task list.

        Returns:
            list[Task]: A list of all Task objects in insertion order.
                        Returns an empty list if no tasks exist.

        Raises:
            None: This method never raises exceptions.

        Behavior:
            - Returns tasks in the order they were added (insertion order)
            - Returns an empty list (not None) when no tasks exist
            - Does not modify the task list
            - Performance: O(n) where n is the number of tasks

        Example:
            >>> service = TaskService()
            >>> tasks = service.get_all_tasks()
            >>> print(f"Found {len(tasks)} tasks")
            Found 3 tasks

        Testing:
            - Test with empty list → returns []
            - Test with 1 task → returns list with 1 task
            - Test with 100 tasks → returns list with 100 tasks in order
            - Test that returned list doesn't alias internal list (immutability)
        """
        ...

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Retrieve a single task by its unique ID.

        Args:
            task_id (int): The unique identifier of the task to retrieve.
                          Must be a positive integer (> 0).

        Returns:
            Task: The Task object with the matching ID.

        Raises:
            ValueError: If task_id <= 0 with message:
                       "ERROR 103: Task ID must be a positive number."
            ValueError: If no task with task_id exists with message:
                       "ERROR 101: Task with ID {task_id} not found."

        Behavior:
            - Validates task_id is positive before searching
            - Searches the task list sequentially for matching ID
            - Returns the first (and only) task with matching ID
            - Does not modify the task list
            - Performance: O(n) where n is the number of tasks

        Error Handling:
            - task_id = 0 → ValueError("ERROR 103: ...")
            - task_id = -5 → ValueError("ERROR 103: ...")
            - task_id = 999 (doesn't exist) → ValueError("ERROR 101: Task with ID 999 not found.")

        Example:
            >>> service = TaskService()
            >>> try:
            ...     task = service.get_task_by_id(5)
            ...     print(f"Found: {task.title}")
            ... except ValueError as e:
            ...     print(f"Error: {e}")
            Found: Buy groceries

        Testing:
            - Test with valid existing ID → returns correct Task
            - Test with ID = 0 → raises ERROR 103
            - Test with ID = -1 → raises ERROR 103
            - Test with non-existent positive ID → raises ERROR 101
            - Test with ID = first task → returns first task
            - Test with ID = last task → returns last task
            - Test error messages match exact format from spec
        """
        ...


# Contract Verification Notes:
# =============================
#
# 1. Type Safety:
#    - All parameters have type hints
#    - Return types are explicit (list[Task] or Task)
#    - Exceptions are documented in raises section
#
# 2. Error Codes:
#    - ERROR 101: Task not found (matches spec FR-014)
#    - ERROR 103: Invalid ID range (matches spec FR-012)
#    - No ERROR 102 in service layer (handled at UI layer during input conversion)
#
# 3. Immutability:
#    - get_all_tasks() should return a copy or immutable view
#    - get_task_by_id() returns a Task object (dataclass, considered immutable for read-only use)
#
# 4. Performance:
#    - Both methods are O(n) linear search
#    - Acceptable for in-memory list with expected small dataset
#    - No indexing or caching needed for Phase I
#
# 5. Null Safety:
#    - get_all_tasks() never returns None (returns empty list instead)
#    - get_task_by_id() never returns None (raises ValueError instead)
#
# 6. Thread Safety:
#    - Not required (single-threaded CLI application)
#    - Not addressed in this contract
#
# 7. Compatibility:
#    - These methods extend existing TaskService
#    - Do not conflict with existing add_task() method from feature 001
#    - Follow same error handling pattern (ValueError with specific messages)
