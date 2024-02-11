"""
recurring.py — utilities for recurring task expansion

STATUS: Work in progress. Not yet integrated with the main CLI flow.
See docs/recurring_spec.md for design intent and remaining open questions.

Checked in as a progress snapshot — M.T. 2024-02-11
"""

from datetime import date, timedelta
from storage import Task

# Supported intervals and their timedeltas.
# "monthly" is deferred — needs careful edge-case handling
# (e.g. Jan 31 + 1 month → Feb 28? Mar 31 + 1 month → Apr 30?).
# TODO: use dateutil.relativedelta or write a custom month_advance() helper.
INTERVALS: dict[str, timedelta] = {
    "daily":  timedelta(days=1),
    "weekly": timedelta(weeks=1),
}


def next_due_date(current_due: str, interval: str) -> str | None:
    """
    Given an ISO 8601 date string and an interval name, return the next
    due date as an ISO 8601 string.

    Returns None if the interval is unsupported.
    """
    if interval not in INTERVALS:
        # TODO: log a warning instead of silently returning None?
        return None
    d = date.fromisoformat(current_due)
    return (d + INTERVALS[interval]).isoformat()


def should_expand(task: Task) -> bool:
    """
    Return True if a recurring task is ready to have a new occurrence created.

    Currently requires:
      - task.recur is set
      - task is marked done
      - task has a due_date (so we know what to advance from)

    TODO: also gate on "haven't already generated an occurrence for this cycle"
          to prevent duplicates if expand is called more than once.
    """
    return bool(task.recur and task.done and task.due_date)


def make_next_occurrence(task: Task, all_tasks: list) -> Task | None:
    """
    Create and return the next Task occurrence for a completed recurring task.

    Returns None if expansion is not applicable or interval is unsupported.
    Caller is responsible for appending the result and calling save_tasks().
    """
    if not should_expand(task):
        return None

    new_due = next_due_date(task.due_date, task.recur)
    if new_due is None:
        return None

    next_task_id = max((t.id for t in all_tasks), default=0) + 1

    return Task(
        id=next_task_id,
        title=task.title,
        done=False,
        priority=task.priority,
        due_date=new_due,
        tags=list(task.tags),
        recur=task.recur,
    )


# TODO: wire make_next_occurrence() into cmd_done in cli.py
# TODO: write unit tests in test_recurring.py
# TODO: decide on monthly handling before marking this module complete
