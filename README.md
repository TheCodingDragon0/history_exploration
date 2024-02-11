# taskr — CLI Task Manager

A simple command-line task manager. Tasks are stored locally in `tasks.json`.

## Requirements

- Python 3.10+
- No external dependencies (standard library only)

## Usage

```
python todo.py <command> [options]
```

### Commands

| Command         | Description                  |
|-----------------|------------------------------|
| `add <title>`   | Add a new task               |
| `list`          | List open tasks              |
| `done <id>`     | Mark a task complete         |
| `delete <id>`   | Delete a task                |

### Options for `add`

| Flag                    | Description                                                  |
|-------------------------|--------------------------------------------------------------|
| `-p, --priority LEVEL`  | Priority: `high`, `medium`, `low`  (default: `medium`)       |
| `-d, --due DATE`        | Due date in `YYYY-MM-DD` format                              |
| `--recur INTERVAL`      | Recurrence: `daily`, `weekly`, `monthly` (**experimental**)  |

### Options for `list`

| Flag               | Description                                         |
|--------------------|-----------------------------------------------------|
| `-f, --filter TEXT`| Show only tasks whose title contains TEXT           |
| `-a, --all`        | Show all tasks including completed ones             |
| `--done`           | Show only completed tasks                           |

## Examples

```bash
python todo.py add "Write project proposal" -p high -d 2024-02-20
python todo.py add "Weekly team sync" --recur weekly -d 2024-02-12
python todo.py list
python todo.py list -f "proposal"
python todo.py done 1
python todo.py delete 3
```

## Storage

Tasks are stored in `tasks.json` in the current working directory. The file
format is versioned; taskr will automatically migrate older formats on load.

> **Note:** Recurring task support (`--recur`) is experimental and not fully
> implemented. The flag stores the field but does **not** yet auto-generate new
> occurrences when a task is completed. See `docs/recurring_spec.md`.
