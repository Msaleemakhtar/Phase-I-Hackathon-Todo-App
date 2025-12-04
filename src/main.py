"""Application entry point and main menu."""

from src.constants import MSG_TASK_ADDED
from src.services.task_service import create_task
from src.ui.prompts import get_task_description, get_task_title


def handle_add_task() -> None:
    """Handle Add Task user flow.

    Prompts user for title and description, validates inputs,
    creates task, and displays success message.
    """
    title = get_task_title()
    description = get_task_description()
    create_task(title, description)
    print(MSG_TASK_ADDED)


def main() -> None:
    """Main application loop."""
    while True:
        print("\n=== Todo App ===")
        print("1. Add Task")
        print("2. View Tasks")  # Future feature
        print("3. Update Task")  # Future feature
        print("4. Delete Task")  # Future feature
        print("5. Mark Complete")  # Future feature
        print("6. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            handle_add_task()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Feature not yet implemented or invalid option.")


if __name__ == "__main__":
    main()
