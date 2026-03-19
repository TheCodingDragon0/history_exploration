# PR #4 — Refactor storage to use Task dataclass

**Branch:** refactor/task-dataclass
**Author:** dev-priya
**Opened:** 2024-02-05
**Merged:** 2024-02-09
**GitHub PR:** #4

---

## Summary

Replaces the raw `dict` representation of tasks with a typed `Task` dataclass.
**This is a purely internal refactor — no user-visible behavior changes.**

---

## Motivation

As we add more fields (priority, due_date, tags, and eventually recur), raw
dict access like `task["due_date"]` is becoming error-prone:

- Typos in key names fail silently at runtime, not at definition time.
- Default values have to be handled at every call site with `task.get(...)`.
- There's no single place to see all the fields a task can have.

A dataclass gives us attribute access, a single schema definition, explicit
defaults, and easier `__repr__` for debugging — all for very little added code.

---

## What changed (commit by commit — please review in order)

**Commit 1** — Define Task dataclass with to_dict and from_dict

Added the `Task` dataclass to `storage.py`. No behavior change yet — the
dataclass exists but nothing uses it. Deliberately isolated so this commit is
reviewable on its own.

**Commit 2** — Migrate storage and CLI to use Task objects; add schema versioning

`load_tasks()` now returns `List[Task]`. `save_tasks()` serializes via
`to_dict()`. v1 bare-list format detected and migrated transparently on load.
CLI updated in the same commit (they must be atomic — swapping storage without
updating the consumer would break the tool).

**Commit 3** — Add CHANGELOG, design notes, and PR description for v0.3.0

Documentation pass for the release.

---

## What this is NOT

This PR does not change the on-disk representation of individual tasks.
The JSON keys and values for each task are identical to before. Only the
wrapper structure changed (added `version` key at top level).

---

## Tradeoffs considered

**`dataclass` vs `TypedDict` vs `NamedTuple`:**
- `NamedTuple` — immutable; rebuilding the object to mark a task done is awkward.
- `TypedDict` — still dict access; doesn't give us defaults or `from_dict`.
- `dataclass` — mutable, supports defaults, generates `__repr__`, serializes
  cleanly with `asdict()`. Clear winner here.

**Adding `tags` now even though it's not in the CLI:**
The field costs nothing and avoids a future schema bump.

---

## Testing

Manually tested all four commands against:
1. Fresh environment (no tasks.json)
2. Existing v1-format tasks.json (bare list) — migration preserves all data
3. Existing v2-format tasks.json — no regressions

No automated tests yet (tracked as a separate item).
