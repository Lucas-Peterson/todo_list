# todo.py

import os
import json

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []

    with open(TASKS_FILE, "r") as file:
        tasks = json.load(file)
    return tasks

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def display_tasks(tasks, level=0, prefix=""):
    if not tasks and level == 0:
        print("No tasks found.")
        return
    
    for index, task in enumerate(tasks):
        connector = "└── " if index == len(tasks) - 1 else "├── "
        if isinstance(task, dict):
            print(f"{prefix}{connector}{task['name']}")
            if 'subtasks' in task and task['subtasks']:
                new_prefix = prefix + ("    " if index == len(tasks) - 1 else "│   ")
                display_tasks(task['subtasks'], level + 1, new_prefix)

def add_task(tasks):
    os.system('cls' if os.name == 'nt' else 'clear')
    task_name = input("Enter a new task: ")
    new_task = {'name': task_name, 'subtasks': []}
    tasks.append(new_task)
    add_subtasks(new_task['subtasks'])
    save_tasks(tasks)
    print(f"Task '{task_name}' added.")

def add_subtasks(subtasks):
    while True:
        subtask_name = input("Enter a subtask (or 'done' to finish): ")
        if subtask_name.lower() == 'done':
            break
        subtasks.append({'name': subtask_name, 'subtasks': []})

def manage_subtasks(tasks):
    os.system('cls' if os.name == 'nt' else 'clear')
    display_tasks(tasks)
    try:
        task_index = int(input("Enter the number of the task to manage subtasks: ")) - 1
        task = get_task_by_index(tasks, task_index)
        if task:
            while True:
                print("\nadd - Add a subtask")
                print("remove - Remove a subtask")
                print("back - Go back")
                choice = input("Enter your choice: ")

                if choice == "add":
                    add_subtasks(task['subtasks'])
                    save_tasks(tasks)
                elif choice == "remove":
                    remove_task(task['subtasks'])
                    save_tasks(tasks)
                elif choice == "back":
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def get_task_by_index(tasks, index, level=0):
    for task in tasks:
        if isinstance(task, dict):
            if index == 0:
                return task
            index -= 1
            if 'subtasks' in task:
                subtask = get_task_by_index(task['subtasks'], index, level + 1)
                if subtask:
                    return subtask
                index -= len(task['subtasks'])
    return None

def remove_task(tasks):
    os.system('cls' if os.name == 'nt' else 'clear')
    display_tasks(tasks)
    try:
        task_index = int(input("Enter the number of the task to remove: ")) - 1
        task_to_remove = get_task_by_index(tasks, task_index)
        if task_to_remove:
            tasks.remove(task_to_remove)
            save_tasks(tasks)
            print(f"Task '{task_to_remove['name']}' removed.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")


def delete_all_tasks():
    os.system('cls' if os.name == 'nt' else 'clear')
    confirmation = input("Are you sure you want to delete all tasks? (y/n): ").lower()
    if confirmation == 'y':
        with open(TASKS_FILE, "w") as file:
            json.dump([], file, indent=4)
        print("All tasks have been deleted.")
    else:
        print("Operation cancelled.")

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    tasks = load_tasks()

    while True:
        print("\nview - View tasks")
        print("add - Add a task")
        print("remove - Remove a task")
        print("managesub - Manage subtasks")
        print("deleteall - Delete all tasks")
        print("exit - Exit")
        choice = input("Enter your choice: ")

        if choice == "view":
            display_tasks(tasks)
        elif choice == "add":
            add_task(tasks)
        elif choice == "remove":
            remove_task(tasks)
        elif choice == "managesub":
            manage_subtasks(tasks)
        elif choice == "deleteall":
            delete_all_tasks()
        elif choice == "exit":
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
