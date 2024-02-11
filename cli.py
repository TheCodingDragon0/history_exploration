import argparse
import sys

from storage import load_tasks, save_tasks, next_id, Task

PRIORITY_LABELS = {1: "high", 2: "medium", 3: "low"}
PRIORITY_VALUES = {
    "high": 1, "h": 1,
    "medium": 2, "m": 2,
    "low": 3, "l": 3,
}


def cmd_add(args):
    tasks = load_tasks()
    priority = PRIORITY_VALUES.get((args.priority or "medium").lower(), 2)
    task = Task(
        id=next_id(tasks),
        title=args.title,
        priority=priority,
        due_date=args.due,
        recur=args.recur,   # stored but expansion not yet triggered
    )
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task.id}: {task.title}")


def cmd_list(args):
    tasks = load_tasks()
    if not tasks:
        print("No tasks.")
        return

    if args.filter:
        tasks = [t for t in tasks if args.filter.lower() in t.title.lower()]

    if args.done_only:
        tasks = [t for t in tasks if t.done]
    elif not args.all:
        tasks = [t for t in tasks if not t.done]

    tasks = sorted(tasks, key=lambda t: (t.priority, t.due_date or "9999-99-99"))

    if not tasks:
        print("No matching tasks.")
        return

    for t in tasks:
        status = "x" if t.done else " "
        pri = PRIORITY_LABELS.get(t.priority, "?")
        due = f"  due:{t.due_date}" if t.due_date else ""
        recur_label = f"  recur:{t.recur}" if t.recur else ""  # display only — no logic yet
        print(f"[{status}] #{t.id:<3}  [{pri:<6}]  {t.title}{due}{recur_label}")


def cmd_done(args):
    tasks = load_tasks()
    for t in tasks:
        if t.id == args.id:
            t.done = True
            # TODO: call expand_recurring here once it's implemented
            save_tasks(tasks)
            print(f"Marked #{t.id} done: {t.title}")
            return
    print(f"Error: task #{args.id} not found.", file=sys.stderr)
    sys.exit(1)


def cmd_delete(args):
    tasks = load_tasks()
    original_count = len(tasks)
    tasks = [t for t in tasks if t.id != args.id]
    if len(tasks) == original_count:
        print(f"Error: task #{args.id} not found.", file=sys.stderr)
        sys.exit(1)
    save_tasks(tasks)
    print(f"Deleted task #{args.id}.")


# ---------------------------------------------------------------------------
# Recurring task expansion — WIP, not yet connected to command flow
# ---------------------------------------------------------------------------

def expand_recurring(tasks):
    """
    After a recurring task is marked done, generate the next occurrence.
    Returns a list of new Task objects to append to the task list.

    TODO: figure out where to call this — from cmd_done? a separate 'sync' command?
    TODO: handle tasks with no due_date
    TODO: implement monthly interval
    """
    new_tasks = []
    for t in tasks:
        if t.recur and t.done:
            pass  # placeholder — date-advance logic lives in recurring.py
    return new_tasks


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="taskr", description="A simple CLI task manager.")
    sub = parser.add_subparsers(dest="command", metavar="command")

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task description")
    p_add.add_argument("-p", "--priority", default="medium", metavar="LEVEL",
                       help="Priority level: high, medium, low  (default: medium)")
    p_add.add_argument("-d", "--due", metavar="DATE", help="Due date in YYYY-MM-DD format")
    p_add.add_argument("--recur", metavar="INTERVAL",
                       help="Recurrence interval: daily, weekly, monthly  [experimental]")

    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("-f", "--filter", metavar="TEXT",
                        help="Show only tasks whose title contains TEXT")
    p_list.add_argument("-a", "--all", action="store_true",
                        help="Include completed tasks in output")
    p_list.add_argument("--done", dest="done_only", action="store_true",
                        help="Show only completed tasks")

    p_done = sub.add_parser("done", help="Mark a task complete")
    p_done.add_argument("id", type=int)

    p_delete = sub.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", type=int)

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
