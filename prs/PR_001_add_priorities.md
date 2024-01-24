# PR #001 — Add priorities and due dates

**Branch:** feature/priorities-and-dates
**Author:** dev-mt
**Opened:** 2024-01-22
**Merged:** 2024-01-24
**Merge commit:** (direct push — no separate PR branch)

---

## Changes

- Added priority field to tasks (high/medium/low, stored as 1/2/3)
- Added due date field to tasks (YYYY-MM-DD format)
- Updated add command with -p and -d flags
- Updated list command to sort by priority
- Fixed bug with missing tasks.json file
- Fixed task ID generation
- Updated README

## Notes

Closes #1 and #2.

Everything tested manually, worked fine on my machine. The priority sorting
feels right. Let me know if you want different defaults.
