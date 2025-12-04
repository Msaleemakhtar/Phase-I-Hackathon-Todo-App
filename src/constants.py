"""Application constants for validation and messaging."""

# Validation limits
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000

# Error codes and messages
ERROR_TITLE_REQUIRED = "ERROR 001: Title is required and must be 1-200 characters."
ERROR_TITLE_TOO_LONG = "ERROR 002: Title is required and must be 1-200 characters."
ERROR_DESCRIPTION_TOO_LONG = "ERROR 003: Description cannot exceed 1000 characters."

# Success messages
MSG_TASK_ADDED = "Task added successfully."

# Prompts
PROMPT_TITLE = "Enter Task Title: "
PROMPT_DESCRIPTION = "Enter Optional Task Description (press Enter to skip): "
