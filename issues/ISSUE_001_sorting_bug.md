# ISSUE #1 — Task list order is inconsistent after mark-done

**GitHub Issue:** #1
**Status:** Closed (fixed in commit after this was filed)
**Opened by:** priya.k
**Date opened:** 2024-01-18
**Date closed:** 2024-01-24

---

## Description

When I run `taskr list`, the order of tasks changes unpredictably after I mark
one done and then list again. Tasks seem to come back in insertion order
sometimes, and in a different order other times.

## Steps to reproduce

```
python todo.py add "Task A"
python todo.py add "Task B"
python todo.py add "Task C"
python todo.py list
# → Task A, Task B, Task C (expected)

python todo.py done 1
python todo.py list
# → sometimes Task B, Task C  (fine)
# → sometimes Task C, Task B  (wrong)
```

I can't reliably reproduce it, but it happens maybe 30% of runs.

## Expected behavior

`taskr list` should return tasks in a stable, predictable order across all
invocations.

## Actual behavior

Order is determined by dict insertion order in the JSON file, which changes
when tasks are rewritten after a `done` or `delete` command.

## Environment

- Python 3.11.2
- macOS 13.4
- tasks.json stored in current directory

## Notes

I suspect the root issue is that `taskr list` has no explicit sort at all — it
just iterates the raw list from the file. Fixing the sort would also let us
implement priority-based listing in the future.

Workaround: none currently.

---

**Comment — dev team (2024-01-20):**
Good catch. Confirmed reproducible. The list command has no sort — file order
is effectively determined by Python's dict insertion order, which changes subtly
when tasks are rewritten after `done`. Fix: add an explicit sort in `cmd_list()`.

**Comment — dev team (2024-01-24):**
Fixed. `cmd_list()` now sorts by `(priority, due_date)`. Closing.
