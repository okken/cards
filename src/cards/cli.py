"""Command Line Interface (CLI) for cards project."""
import json
import os
import pathlib
from typing import List

import cards
import typer
from tabulate import tabulate

DEFAULT_TABLEFORMAT = os.environ.get("CARDSTABLEFORMAT", "simple")

app = typer.Typer()


@app.command()
def version():
    """Return version of cards application"""
    print(cards.__version__)


@app.command()
def add(
    summary: List[str],
    owner: str = typer.Option(None, "-o", "--owner", help="set the card owner"),
):
    """Add a card to db."""
    set_cards_db_path()
    summary = " ".join(summary) if summary else None
    cards.add_card(cards.Card(summary, owner))


@app.command()
def delete(card_id: int):
    """Remove card in db with given id."""
    set_cards_db_path()
    cards.delete_card(card_id)


@app.command("list")
def list_cards(
    noowner: bool = typer.Option(
        None, "-n", "--noowner", "--no-owner", help="list cards without owners",
    ),
    owner: str = typer.Option(None, "-o", "--owner", help="filter on the cards owner"),
    priority: int = typer.Option(
        None, "-p", "--priority", help="fliter on this priority and above",
    ),
    done: bool = typer.Option(
        None, "-d", "--done", help="filter on cards with given done state",
    ),
    format: str = typer.Option(
        DEFAULT_TABLEFORMAT,
        "-f",
        "--format",
        help='table fomratting option, eg. "grid", "simple", "html"',
    ),
):
    """
    List cards in db.
    """
    set_cards_db_path()
    filter = {"noowner": noowner, "owner": owner, "priority": priority, "done": done}
    the_cards = cards.list_cards(filter=filter)

    #  json is a special case
    if format == "json":
        items = [c.to_dict() for c in the_cards]
        print(json.dumps({"cards": items}, sort_keys=True, indent=4))
        return

    # who's going to remember 'pipe' for markdown?
    if format == "markdown":
        format = "pipe"

    if format == "packed":
        for t in the_cards:
            done = "x" if t.done else "o"
            owner = "unassigned" if t.owner is None else t.owner
            line = f"{t.id} {owner} {t.priority} {done} {t.summary}"
            print(line)
        return

    # all formats except json/none use tabulate
    items = []
    for t in the_cards:
        done = " x " if t.done else ""
        owner = "" if t.owner is None else t.owner
        items.append((t.id, owner, t.priority, done, t.summary))

    print(
        tabulate(
            items,
            headers=("ID", "owner", "priority", "done", "summary"),
            tablefmt=format,
        ),
    )


@app.command()
def update(
    card_id: int,
    owner: str = typer.Option(None, "-o", "--owner", help="change the card owner"),
    priority: int = typer.Option(
        None, "-p", "--priority", help="change the card priority",
    ),
    summary: List[str] = typer.Option(
        None, "-s", "--summary", help="change the card summary",
    ),
    done: bool = typer.Option(None, "-d", "--done", help="change the card done state"),
):
    """Modify a card in db with given id with new info."""
    set_cards_db_path()
    summary = " ".join(summary) if summary else None
    cards.update_card(card_id, cards.Card(summary, owner, priority, done))


@app.command()
def count(
    noowner: bool = typer.Option(
        None, "-n", "--noowner", "--no-owner", help="count cards without owners",
    ),
    owner: str = typer.Option(
        None, "-o", "--owner", help="count cards with given owner",
    ),
    priority: int = typer.Option(
        None, "-p", "--priority", help="count cards with given priority",
    ),
    done: bool = typer.Option(
        None, "-d", "--done", help="count cards with given done state (True or False)",
    ),
):
    """Return number of cards in db."""
    set_cards_db_path()
    print(cards.count(noowner, owner, priority, done))


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Call list_cards of nothing else
    """
    if ctx.invoked_subcommand is None:
        list_cards(
            noowner=None,
            owner=None,
            priority=None,
            done=None,
            format=DEFAULT_TABLEFORMAT,
        )


def set_cards_db_path():
    # just put it in users home dir for now
    db_path = pathlib.Path().home() / ".cards_db.json"
    cards.set_db_path(db_path)


# useful for debugging during development
# doesn't need test coverage
if __name__ == "__main__":
    app()  # pragma: no cover
