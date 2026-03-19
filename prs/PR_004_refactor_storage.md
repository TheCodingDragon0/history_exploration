# PR #4 — Refactor storage to use Task dataclass

**Author:** dev-priya  |  **Merged:** 2024-02-09  |  **Strategy:** merge commit

## Summary

Replaces raw `dict` task representation with a typed `Task` dataclass.
**No user-visible behavior changes.**

## Motivation

As fields multiply (priority, due_date, tags, recur), raw dict access like
`task["due_date"]` is error-prone: typos fail silently, defaults must be
handled at every call site, and there is no single place to see the schema.
A dataclass gives attribute access, explicit defaults, and a clear definition.

## Tradeoffs considered

**`dataclass` vs `TypedDict` vs `NamedTuple`:**
- `NamedTuple` — immutable; rebuilding the whole object to mark a task done
  is awkward.
- `TypedDict` — still dict access; doesn't give us defaults or `from_dict`.
- `dataclass` — mutable, supports defaults, generates `__repr__`, serializes
  cleanly with `asdict()`. Clear winner for this use case.

**Adding `tags` now even though it's not in the CLI:**
The field costs nothing and avoids a future schema bump.

## Schema versioning

`tasks.json` now includes `"version": 2`. Existing v1 files (bare lists) are
detected and migrated transparently on load — no manual migration step.

## Reviewer comment

> Did you consider using `__post_init__` to validate the `priority` field
> (reject values outside 1–3)? Might be worth a follow-up issue rather than
> scope-creeping this PR.
