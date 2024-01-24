# ISSUE #002 — Due dates

**Status:** Closed (implemented in commit `2e1d0c9`)
**Opened by:** tom.w
**Date opened:** 2024-01-22
**Date closed:** 2024-01-26

---

## Description

Can we have due dates?

## Notes

It would be nice.

Would be useful for work stuff.

---

**Comment — dev team (2024-01-23):**

Tom, can you give us a bit more detail? Specifically:

- What format should due dates use? (YYYY-MM-DD? MM/DD/YYYY? Natural language
  like "friday"?)
- Should the list command warn when a task is overdue?
- Should overdue tasks sort differently — e.g. always at the top?
- Is this a `taskr add` flag, or do you want a separate `taskr due <id> <date>`
  command for setting due dates on existing tasks?

---

**Comment — tom.w (2024-01-23):**

idk just like a date field. iso format maybe

---

**Comment — dev team (2024-01-24):**

Ok. We'll go with ISO 8601 (`YYYY-MM-DD`) for now, added as a `-d / --due`
flag on `taskr add`. Overdue highlighting is a separate feature — not adding it
in this pass. If you need to set a due date on an existing task, delete and
re-add for now.

---

**Comment — dev team (2024-01-26):**

Implemented in commit `2e1d0c9` with PR #7. Closing. If you want overdue
highlighting or a `taskr due <id>` command, please open a new issue with more
detail about what you'd find useful.
