from pathlib import Path
from datetime import datetime
import json


# Main project folder: TodoVaultCLI/
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# File where tasks will be saved
TASKS_FILE = PROJECT_ROOT / "data" / "tasks.json"


def load_tasks():
    """
    Loads tasks from data/tasks.json.
    If file does not exist, returns empty list.
    """

    if not TASKS_FILE.exists():
        return []

    with open(TASKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks):
    """
    Saves all tasks to data/tasks.json.
    """

    TASKS_FILE.parent.mkdir(exist_ok=True)

    with open(TASKS_FILE, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def get_next_id(tasks):
    """
    Finds next task ID.
    If no tasks exist, first ID is 1.
    """

    if not tasks:
        return 1

    return max(task["id"] for task in tasks) + 1


def add_task(tasks):
    """
    Adds a new task.
    """

    title = input("Enter task title: ").strip()

    if not title:
        print("Task title cannot be empty.")
        return

    priority = input("Enter priority low/medium/high: ").strip().lower()

    if priority not in ["low", "medium", "high"]:
        priority = "medium"

    task = {
        "id": get_next_id(tasks),
        "title": title,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    tasks.append(task)
    save_tasks(tasks)

    print("Task added successfully.")


def list_tasks(tasks):
    """
    Shows all tasks.
    """

    if not tasks:
        print("No tasks found.")
        return

    print("\n==============================")
    print(" YOUR TASKS")
    print("==============================")

    for task in tasks:
        status = "DONE" if task["completed"] else "TODO"

        print(f"\nID: {task['id']}")
        print(f"Title: {task['title']}")
        print(f"Priority: {task['priority']}")
        print(f"Status: {status}")
        print(f"Created: {task['created_at']}")


def complete_task(tasks):
    """
    Marks a task as completed.
    """

    try:
        task_id = int(input("Enter task ID to complete: "))
    except ValueError:
        print("Invalid ID.")
        return

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print("Task marked as completed.")
            return

    print("Task not found.")


def delete_task(tasks):
    """
    Deletes a task by ID.
    """

    try:
        task_id = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print("Task deleted.")
            return

    print("Task not found.")


def search_tasks(tasks):
    """
    Searches tasks by title.
    """

    keyword = input("Enter search keyword: ").strip().lower()

    if not keyword:
        print("Search cannot be empty.")
        return

    found_tasks = [
        task for task in tasks
        if keyword in task["title"].lower()
    ]

    if not found_tasks:
        print("No matching tasks found.")
        return

    list_tasks(found_tasks)


def show_stats(tasks):
    """
    Shows task statistics.
    """

    total = len(tasks)
    completed = len([task for task in tasks if task["completed"]])
    remaining = total - completed

    high_priority = len([task for task in tasks if task["priority"] == "high"])
    medium_priority = len([task for task in tasks if task["priority"] == "medium"])
    low_priority = len([task for task in tasks if task["priority"] == "low"])

    print("\n==============================")
    print(" TASK STATS")
    print("==============================")
    print(f"Total tasks: {total}")
    print(f"Completed: {completed}")
    print(f"Remaining: {remaining}")
    print(f"High priority: {high_priority}")
    print(f"Medium priority: {medium_priority}")
    print(f"Low priority: {low_priority}")


def show_menu():
    """
    Prints main menu.
    """

    print("\n==============================")
    print(" TODO VAULT CLI")
    print("==============================")
    print("1. Add task")
    print("2. List tasks")
    print("3. Complete task")
    print("4. Delete task")
    print("5. Search tasks")
    print("6. Show stats")
    print("7. Exit")


def main():
    """
    Program starts here.
    """

    tasks = load_tasks()

    while True:
        show_menu()

        choice = input("Choose option: ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            search_tasks(tasks)
        elif choice == "6":
            show_stats(tasks)
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Choose 1-7.")


if __name__ == "__main__":
    main()