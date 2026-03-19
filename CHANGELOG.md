# Changelog

All notable changes to taskr are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

### In progress
- Recurring task support (`--recur daily/weekly/monthly`) — feature incomplete,
  do not rely on in production. See `docs/recurring_spec.md`.

---

## [0.3.0] — 2024-02-09

### Changed
- Refactored internal storage to use a typed `Task` dataclass (PR #4).
  No change to user-visible behavior.
- `tasks.json` now includes a top-level `"version": 2` field for forward
  compatibility. Existing v1 files (bare lists) are migrated transparently
  on first load.

---

## [0.2.0] — 2024-01-28

### Added
- `--filter` / `-f` flag for `taskr list`: show only tasks whose title
  contains the given text (case-insensitive). (PR #3)

---

## [0.1.1] — 2024-01-24

### Added
- Task priorities: `-p high / medium / low` on `taskr add`.
  Stored as integers (1/2/3) for reliable sorting.
- Due dates: `-d YYYY-MM-DD` on `taskr add`.
- `taskr list` now sorts by priority (ascending), then due date (ascending).
  Tasks without a due date sort to the end.

### Fixed
- `taskr list` no longer crashes when `tasks.json` does not exist. (issue #1)
- Task IDs now use `max(existing ids) + 1` instead of `count + 1`, which
  previously caused ID collisions after deletions.

---

## [0.1.0] — 2024-01-15

### Added
- Initial release.
- `taskr add <title>` — add a task.
- `taskr list` — list open tasks.
- `taskr done <id>` — mark a task complete.
- `taskr delete <id>` — delete a task.
- Tasks stored as JSON in `tasks.json`.
