import json

TASKS_FILE = "tasks.json"


def load_tasks():
    with open(TASKS_FILE, "r") as f:   # crashes if file doesn't exist yet
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def next_id(tasks):
    return len(tasks) + 1
