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


def build_parser():
    parser = argparse.ArgumentParser(prog="taskr", description="A simple CLI task manager.")
    sub = parser.add_subparsers(dest="command", metavar="command")

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task description")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    if args.command == "add":
        cmd_add(args)
