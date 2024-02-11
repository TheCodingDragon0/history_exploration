# Recurring Tasks — Design Spec

**Author:** M.T.
**Status:** In Progress
**Last updated:** 2024-02-11

---

## Motivation

Several people have asked for repeating tasks (e.g., "check server backups
every Monday", "weekly team sync"). Right now, users have to manually re-add
the same task after completing it, which is annoying and easy to forget.

---

## Proposed behavior

A task with `recur: "weekly"` should, when marked done:

1. Stay in the completed state for the current occurrence.
2. Automatically generate a new open copy of the task with:
   - `done: false`
   - `due_date` advanced by the recurrence interval
   - Same `title`, `priority`, `tags`, and `recur` value as the original

---

## Intervals

| Value     | Advance by          |
|-----------|---------------------|
| `daily`   | 1 day               |
| `weekly`  | 7 days              |
| `monthly` | ~1 month (TBD — see open questions) |

---

## Open questions

**1. When does expansion happen?**
At mark-done time (eager), or at list time (lazy)?

- Lean toward **mark-done time** for simplicity — the user just ran `taskr done`,
  so it's natural to generate the next occurrence right then.
- Lazy expansion (at `taskr list`) would require tracking whether an occurrence
  has already been generated, to avoid creating duplicates on every list call.

**2. What if the task has no `due_date`?**
Recurring without a due date doesn't really make sense — you can't advance a
date you don't have. Proposal: skip expansion silently. Maybe warn the user.

**3. Monthly edge cases.**
Feb 28 + 1 month = Mar 28? What about Jan 31 + 1 month?
- Option A: Use `dateutil.relativedelta` (external dep — avoid if possible).
- Option B: Roll our own `month_advance()` with explicit clamping.
- Option C: Defer monthly support until there's a clear user need.

**4. Preventing duplicate generation.**
If `cmd_done` calls `make_next_occurrence()` and the user runs `done` twice on
the same task (bug or accidental re-run), we'd generate two occurrences.
Need a guard — maybe a `recur_parent_id` field, or check if an open task with
the same title+recur already exists.

---

## Storage changes

The `recur` field has been added to the `Task` dataclass in `storage.py`.
Schema version stays at **2** — `recur: null` is the default for all existing
tasks, so no migration is needed.

---

## Implementation checklist

- [x] Add `recur` field to `Task` dataclass (`storage.py`)
- [x] Add `--recur` flag to `taskr add` (`cli.py`)
- [x] Display `recur` label in `taskr list` output (cosmetic only)
- [x] Stub out `recurring.py` with `next_due_date()`, `should_expand()`,
      `make_next_occurrence()`
- [ ] Implement `next_due_date()` for `daily` and `weekly` — **done in
      recurring.py but not called from anywhere**
- [ ] Wire `make_next_occurrence()` into `cmd_done` in `cli.py`
- [ ] Handle `monthly` interval
- [ ] Handle tasks with no `due_date`
- [ ] Guard against duplicate generation
- [ ] Write unit tests (`test_recurring.py`)

---

## Files touched

- `storage.py` — added `recur` field
- `cli.py` — added `--recur` to arg parser; added display in `cmd_list`;
  `expand_recurring()` stub (not called)
- `recurring.py` — new file, partially implemented
- `docs/recurring_spec.md` — this file
