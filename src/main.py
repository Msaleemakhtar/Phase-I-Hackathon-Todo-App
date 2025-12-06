"""Application entry point and main menu."""

from src.constants import MSG_TASK_ADDED
from src.services.task_service import create_task, get_all_tasks, get_task_by_id
from src.ui.prompts import (
    delete_task_prompt,
    display_task_details,
    display_task_list,
    get_task_description,
    get_task_title,
    prompt_for_task_id,
    update_task_prompt,
)


def handle_add_task() -> None:
    """Handle Add Task user flow.

    Prompts user for title and description, validates inputs,
    creates task, and displays success message.
    """
    title = get_task_title()
    description = get_task_description()
    create_task(title, description)
    print(MSG_TASK_ADDED)


def handle_view_tasks() -> None:
    """Handle View Tasks user flow.

    Retrieves all tasks and displays them in a formatted list
    with completion indicators and pagination.
    """
    tasks = get_all_tasks()
    display_task_list(tasks)


def handle_view_task_details() -> None:
    """Handle View Task Details user flow.

    Prompts user for task ID, validates input, retrieves task,
    and displays detailed information. Handles errors gracefully.
    """
    try:
        task_id = prompt_for_task_id()
        task = get_task_by_id(task_id)
        display_task_details(task)
    except ValueError as e:
        print(e)


def main() -> None:
    """Main application loop."""
    while True:
        print("\n=== Todo App ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. View Task Details")
        print("4. Update Task")
        print("5. Delete Task")
        print("6. Mark Complete")  # Future feature
        print("7. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            handle_add_task()
        elif choice == "2":
            handle_view_tasks()
        elif choice == "3":
            handle_view_task_details()
        elif choice == "4":
            update_task_prompt()
        elif choice == "5":
            delete_task_prompt()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Feature not yet implemented or invalid option.")


if __name__ == "__main__":
    main()
