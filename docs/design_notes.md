# Design Notes — taskr

**Last updated:** 2024-02-01

> **Note:** This document was last updated before the storage refactor (PR #4,
> merged 2024-02-09). The "Task representation" section below now describes the
> current state accurately, but some inline code snippets may still reflect the
> old dict-based approach. Treat the source files as authoritative.

---

## Goals

taskr is meant to be:

- **Small:** no external dependencies; single-file-per-concern.
- **Local:** all data lives in a JSON file in the working directory.
- **Readable:** the JSON file should be human-readable and hand-editable in a pinch.
- **Obvious:** a new contributor should be able to understand the full codebase
  in under 30 minutes.

---

## Architecture

```
todo.py        — thin entry point; delegates immediately to cli.main()
cli.py         — argument parsing and command dispatch
storage.py     — JSON persistence layer; owns the Task dataclass
recurring.py   — recurring task utilities (WIP — not yet integrated)
tasks.json     — data file; auto-created on first `taskr add`
```

---

## Task representation

**Current (v2):** Tasks are represented as `Task` dataclasses defined in
`storage.py`.

Fields:

| Field       | Type            | Default  | Notes                                    |
|-------------|-----------------|----------|------------------------------------------|
| `id`        | `int`           | —        | Auto-assigned; uses max+1, not count+1   |
| `title`     | `str`           | —        | Required                                 |
| `done`      | `bool`          | `False`  |                                          |
| `priority`  | `int`           | `2`      | 1=high, 2=medium, 3=low                  |
| `due_date`  | `str` or `None` | `None`   | ISO 8601 (YYYY-MM-DD)                    |
| `tags`      | `List[str]`     | `[]`     | Defined but not yet exposed in CLI       |
| `recur`     | `str` or `None` | `None`   | WIP — see `docs/recurring_spec.md`       |

~~**Original (v1):** Tasks were plain Python dicts with only `id`, `title`,
`done`.~~
*(v1 files are still readable — `load_tasks()` detects and migrates them.)*

---

## Storage format (v2)

```json
{
  "version": 2,
  "tasks": [
    {
      "id": 1,
      "title": "Example task",
      "done": false,
      "priority": 2,
      "due_date": "2024-02-15",
      "tags": [],
      "recur": null
    }
  ]
}
```

Priority encoding: `1` = high, `2` = medium, `3` = low.
Lower number = higher priority; this allows `sorted()` to work directly on the
field without a custom comparator.

---

## Sorting

`taskr list` sorts by `(priority, due_date)` ascending.
Tasks with no due date use the sentinel value `"9999-99-99"` so they sort to
the end.

---

## Design decisions

### Why JSON and not SQLite?

JSON is human-readable and portable with zero setup. For a single-user CLI tool
with tens or hundreds of tasks, SQLite is overkill and adds friction (the file
is less inspectable without tooling). If taskr ever gains multi-user or network
features, reconsider.

### Why not use Click or Typer?

No external dependencies means installation is trivial (`python todo.py add
"thing"` just works). The argparse surface is small enough to be manageable,
and the explicit `dispatch` dict in `cli.main()` keeps the command routing
readable.

### Why integer priorities instead of string labels?

Allows `sorted()` to work directly on the `priority` field. String labels
(`high`, `medium`, `low`) are only used at the input and display layers.
Mapping happens in `PRIORITY_VALUES` and `PRIORITY_LABELS` in `cli.py`.

---

## Future work

*(Not committed to, roughly in priority order)*

- **Recurring tasks** — in progress; see `docs/recurring_spec.md`
- **Overdue highlighting** — `taskr list` could mark overdue items in red
- **Tag filtering** — `taskr list --tag <tag>`; field exists in storage already
- **Import/export** — CSV or other formats for external tooling
- **Config file** — user-level defaults for sort order, date format, file path
