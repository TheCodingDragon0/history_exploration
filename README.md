# taskr — CLI Task Manager

A simple command-line task manager. Tasks are stored locally in `tasks.json`.

## Requirements

- Python 3.10+

## Usage

    python todo.py <command> [options]

### Commands

| Command         | Description                  |
|-----------------|------------------------------|
| `add <title>`   | Add a new task               |
| `list`          | List open tasks (sorted by priority) |
| `done <id>`     | Mark a task complete         |
| `delete <id>`   | Delete a task                |

### Options for `add`

| Flag                   | Description                                           |
|------------------------|-------------------------------------------------------|
| `-p, --priority LEVEL` | Priority: `high`, `medium`, `low`  (default: `medium`) |
| `-d, --due DATE`       | Due date in `YYYY-MM-DD` format                       |

## Examples

```bash
python todo.py add "Write project proposal" -p high -d 2024-02-20
python todo.py list
python todo.py done 1
python todo.py delete 3
```

## Storage

Tasks are stored in `tasks.json` in the current working directory.
