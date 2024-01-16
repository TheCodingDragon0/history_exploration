import argparse
import sys

from storage import load_tasks, save_tasks, next_id


def cmd_add(args):
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "title": args.title,
        "done": False,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {task['title']}")


def cmd_list(args):
    tasks = load_tasks()
    if not tasks:
        print("No tasks.")
        return
    open_tasks = [t for t in tasks if not t["done"]]
    if not open_tasks:
        print("No open tasks.")
        return
    for t in open_tasks:
        print(f"[ ] #{t['id']}  {t['title']}")


def cmd_done(args):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == args.id:
            t["done"] = True
            save_tasks(tasks)
            print(f"Marked #{t['id']} done.")
            return
    print(f"Error: task #{args.id} not found.", file=sys.stderr)
    sys.exit(1)


def cmd_delete(args):
    tasks = load_tasks()
    original_count = len(tasks)
    tasks = [t for t in tasks if t["id"] != args.id]
    if len(tasks) == original_count:
        print(f"Error: task #{args.id} not found.", file=sys.stderr)
        sys.exit(1)
    save_tasks(tasks)
    print(f"Deleted task #{args.id}.")


def build_parser():
    parser = argparse.ArgumentParser(prog="taskr", description="A simple CLI task manager.")
    sub = parser.add_subparsers(dest="command", metavar="command")

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task description")

    p_list = sub.add_parser("list", help="List open tasks")

    p_done = sub.add_parser("done", help="Mark a task complete")
    p_done.add_argument("id", type=int, help="Task ID")

    p_delete = sub.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", type=int, help="Task ID")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    dispatch = {
        "add":    cmd_add,
        "list":   cmd_list,
        "done":   cmd_done,
        "delete": cmd_delete,
    }
    fn = dispatch.get(args.command)
    if fn:
        fn(args)
