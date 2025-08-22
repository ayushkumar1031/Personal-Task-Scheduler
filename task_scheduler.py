# task_scheduler.py
# Personal Task Scheduler
# Author: Ayush Kumar
# Allows adding, viewing, deleting tasks with optional reminders

import json
import os
import time
from datetime import datetime
try:
    from plyer import notification  # Optional: for desktop notifications
except:
    notification = None

TASK_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# Add a new task
def add_task():
    title = input("Enter task title: ")
    due_date = input("Enter due date (YYYY-MM-DD HH:MM, optional): ")
    task = {"title": title, "due_date": due_date, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")}
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task '{title}' added successfully!")

# View all tasks
def view_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['title']} | Due: {task.get('due_date', 'N/A')} | Created: {task['created_at']}")

# Delete a task
def delete_task():
    view_tasks()
    tasks = load_tasks()
    if not tasks:
        return
    try:
        task_num = int(input("Enter task number to delete: "))
        removed = tasks.pop(task_num - 1)
        save_tasks(tasks)
        print(f"Task '{removed['title']}' deleted successfully!")
    except (ValueError, IndexError):
        print("Invalid task number.")

# Check for due tasks and notify
def check_due_tasks():
    if notification is None:
        return
    tasks = load_tasks()
    now = datetime.now()
    for task in tasks:
        due = task.get("due_date")
        if due:
            try:
                due_dt = datetime.strptime(due, "%Y-%m-%d %H:%M")
                if now >= due_dt:
                    notification.notify(
                        title="Task Reminder",
                        message=f"Task '{task['title']}' is due!",
                        timeout=5
                    )
            except:
                continue

# Main menu
def main():
    while True:
        print("\nPersonal Task Scheduler")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Delete Task")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            delete_task()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice, try again.")
        check_due_tasks()
        time.sleep(1)

if __name__ == "__main__":
    main()
