from __future__ import annotations

import json
import pathlib
from typing import Annotated, Optional

import typer
import yaml

from . import OmnivoreAPI

CONFIG_PATH = pathlib.Path.home() / ".config" / "omnivore-api" / "config.yaml"
DEFAULT_API_URL = "https://api-prod.omnivore.app/api/graphql"

app = typer.Typer(help="Omnivore API CLI")


def _load_config() -> OmnivoreAPI:
    if not CONFIG_PATH.exists():
        typer.echo(f"Config file not found: {CONFIG_PATH}", err=True)
        typer.echo("Run `omnivore init` to create it.", err=True)
        raise typer.Exit(code=1)
    config = yaml.safe_load(CONFIG_PATH.read_text())
    api_token = config.get("api_token")
    api_url = config.get("api_url", DEFAULT_API_URL)
    if not api_token:
        typer.echo("Missing `api_token` in config file.", err=True)
        raise typer.Exit(code=1)
    return OmnivoreAPI(api_token, api_url)


@app.command()
def init():
    """Interactive setup: create ~/.config/omnivore-api/config.yaml."""
    api_token = typer.prompt("API token")
    api_url = typer.prompt("API URL", default=DEFAULT_API_URL)
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(
        yaml.dump({"api_token": api_token, "api_url": api_url}, allow_unicode=True)
    )
    typer.echo(f"Config written to {CONFIG_PATH}")


@app.command("save-url")
def save_url(
    url: Annotated[str, typer.Argument(help="URL to save")],
    label: Annotated[Optional[list[str]], typer.Option(help="Label to apply (repeatable)")] = None,
):
    """Save a URL to Omnivore."""
    client = _load_config()
    result = client.save_url(url, labels=label or [])
    typer.echo(json.dumps(result, indent=2, ensure_ascii=False))


@app.command("get-articles")
def get_articles(
    limit: Annotated[Optional[int], typer.Option(help="Max number of articles to return")] = None,
    after: Annotated[int, typer.Option(help="Cursor offset")] = 0,
    query: Annotated[str, typer.Option(help="Search query")] = "in:inbox",
    format: Annotated[str, typer.Option(help="Output format: html or markdown")] = "html",
):
    """List articles from Omnivore."""
    client = _load_config()
    result = client.get_articles(limit=limit, after=after, query=query, format=format)
    typer.echo(json.dumps(result, indent=2, ensure_ascii=False))


@app.command("get-profile")
def get_profile():
    """Get the current user's profile."""
    client = _load_config()
    result = client.get_profile()
    typer.echo(json.dumps(result, indent=2, ensure_ascii=False))


@app.command("get-labels")
def get_labels():
    """List all labels for the current user."""
    client = _load_config()
    result = client.get_labels()
    typer.echo(json.dumps(result, indent=2, ensure_ascii=False))


def main():
    app()
