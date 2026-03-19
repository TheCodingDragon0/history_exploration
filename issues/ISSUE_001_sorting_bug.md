# Issue #1 — Task list order is inconsistent after mark-done

**Status:** Closed
**Opened by:** priya.k

## Description

When I run `taskr list`, the order of tasks changes unpredictably after I mark
one done and run list again.

## Steps to reproduce

```
python todo.py add "Task A"
python todo.py add "Task B"
python todo.py add "Task C"
python todo.py list      # → A, B, C

python todo.py done 1
python todo.py list      # → sometimes B, C / sometimes C, B
```

Can't reliably reproduce it, but happens maybe 30% of runs.

## Expected behavior

`taskr list` should return tasks in a stable, predictable order.

## Actual behavior

Order is determined by dict insertion order in the JSON file, which changes
when tasks are rewritten after a `done` or `delete` command.

## Environment

- Python 3.11.2 / macOS 13.4

## Notes

I suspect `taskr list` has no explicit sort — it just iterates the raw list
from the file. Fixing the sort would also let us implement priority-based
listing in the future.

---

**dev team:** Confirmed. The list command has no sort — fix will be to add an
explicit `sorted()` call in `cmd_list()`.

**dev team (closed):** Fixed. `cmd_list()` now sorts by `(priority, due_date)`.
