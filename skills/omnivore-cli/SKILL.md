---
name: omnivore-cli
description: Interact with the Omnivore read-later service via the `omnivore` CLI. Covers setup, saving URLs, fetching articles/profile/labels, extending the CLI with new commands, and modifying omnivore_api/cli.py. Use when the user asks to use, test, or extend the omnivore CLI tool.
---

# Omnivore CLI

## Overview

The `omnivore` CLI is a typer-based command-line tool provided by the `omnivore_api` Python package.

Entry point: `omnivore_api/cli.py` → registered as `omnivore` via `[project.scripts]` in `pyproject.toml`.

## First-time Setup

```bash
omnivore init
# prompts for API token and API URL
# writes to ~/.config/omnivore-api/config.yaml
```

Config file format (`~/.config/omnivore-api/config.yaml`):

```yaml
api_token: "your-token-here"
api_url: "https://api-prod.omnivore.app/api/graphql"
```

## Available Commands

| Command | Description | Key options |
|---------|-------------|-------------|
| `omnivore init` | Interactive config setup | — |
| `omnivore save-url <url>` | Save a URL | `--label` (repeatable) |
| `omnivore get-articles` | List inbox articles | `--limit`, `--after`, `--query`, `--format` |
| `omnivore get-profile` | Current user info | — |
| `omnivore get-labels` | All labels | — |

All read commands output **JSON** to stdout.

## Usage Examples

```bash
# Save with labels
omnivore save-url https://example.com --label reading --label python

# Paginated fetch, markdown format
omnivore get-articles --limit 20 --after 20 --format markdown

# Filter by date range (Omnivore search syntax)
omnivore get-articles --query "in:inbox published:2024-01-01..*"

# Pipe to jq
omnivore get-labels | jq '.[].name'
```

## Adding a New CLI Command

1. Open `omnivore_api/cli.py`
2. Add a new function decorated with `@app.command("command-name")`
3. Use `Annotated` + `typer.Option` / `typer.Argument` for parameters
4. Call the corresponding `OmnivoreAPI` method via `_load_config()`
5. Output with `typer.echo(json.dumps(result, indent=2))`

Example skeleton:

```python
@app.command("delete-article")
def delete_article(
    article_id: Annotated[str, typer.Argument(help="Article ID")],
):
    """Delete an article from Omnivore."""
    client = _load_config()
    result = client.delete_article(article_id)
    typer.echo(json.dumps(result, indent=2))
```
