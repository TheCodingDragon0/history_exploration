# Issue #5 — --recur flag stores value but never creates new task occurrences

**Status:** Open
**Opened by:** (unknown)

## Description

The `--recur` flag is accepted and the value shows in `taskr list`, but when I
mark the task done, no new occurrence is created.

## Steps to reproduce

```
python todo.py add "Weekly team sync" --recur weekly -d 2024-02-05
python todo.py done 1
python todo.py list
# No open tasks. Expected a new "Weekly team sync" due 2024-02-12.
```

## Notes

Checked `tasks.json` — `recur: "weekly"` is stored correctly. The problem is
in the behavior, not storage.

Looking at the code: `recurring.py` exists and has what looks like the right
logic (`make_next_occurrence`, `next_due_date`), but it's never imported
anywhere. `cmd_done` in `cli.py` has a comment that says
`# TODO: call expand_recurring here once it's implemented`.

This is a known WIP, not an unknown bug. Filing so it doesn't get lost.
