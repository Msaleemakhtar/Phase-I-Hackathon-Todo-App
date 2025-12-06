"""Application constants for validation and messaging."""

# Validation limits
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000

# Error codes and messages - Add Task feature
ERROR_TITLE_REQUIRED = "ERROR 001: Title is required and must be 1-200 characters."
ERROR_TITLE_TOO_LONG = "ERROR 002: Title is required and must be 1-200 characters."
ERROR_DESCRIPTION_TOO_LONG = "ERROR 003: Description cannot exceed 1000 characters."

# Error codes and messages - View Task feature
ERROR_TASK_NOT_FOUND = "ERROR 101: Task with ID {task_id} not found."
ERROR_INVALID_INPUT = "ERROR 102: Invalid input. Please enter a numeric task ID."
ERROR_INVALID_TASK_ID = "ERROR 103: Task ID must be a positive number."

# Success messages
MSG_TASK_ADDED = "Task added successfully."

# Prompts - Add Task feature
PROMPT_TITLE = "Enter Task Title: "
PROMPT_DESCRIPTION = "Enter Optional Task Description (press Enter to skip): "

# Prompts - View Task feature
PROMPT_TASK_ID = "Enter Task ID: "
PROMPT_PAGINATION = "Press Enter to continue..."
MSG_NO_TASKS = "No tasks found."
