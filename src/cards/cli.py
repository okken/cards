"""Command Line Interface (CLI) for cards project."""
import os
from io import StringIO
import pathlib
import rich
from rich.table import Table
from rich.box import SIMPLE
from contextlib import contextmanager
from typing import List, Optional

import cards
from cards.remote import OwnerNotFound, RemoteCardsDB, RemoteError

import typer

app = typer.Typer(add_completion=False)


@app.command()
def version():
    """Return version of cards application"""
    print(cards.__version__)


@app.command()
def add(
    summary: List[str],
    owner: str = typer.Option(None, "-o", "--owner"),
    later: bool = typer.Option(False, "-l", "--later", help="Put the card on the Later list."),
):
    """Add a card to db."""
    summary_str = " ".join(summary) if summary else None
    with cards_db() as db:
        with_owner_check(
            owner,
            lambda owner: db.add_card(
                cards.Card(summary_str, owner, state="todo", later=later or None)
            ),
        )


@app.command()
def delete(card_id: int):
    """Remove card in db with given id."""
    with cards_db() as db:
        try:
            db.delete_card(card_id)
        except cards.InvalidCardId:
            print(f"Error: Invalid card id {card_id}")


@app.command("list")
def list_cards(
    owner: Optional[str] = typer.Option(None, "-o", "--owner"),
    state: Optional[str] = typer.Option(None, "-s", "--state"),
    later: bool = typer.Option(False, "-l", "--later", help="Show the Later list."),
    all_lists: bool = typer.Option(False, "-a", "--all", help="Show both the Sooner and Later lists."),
):
    """
    List cards in db (the Sooner list, unless --later or --all).
    """
    with cards_db() as db:
        matching = with_owner_check(
            owner, lambda owner: db.list_cards(owner=owner, state=state)
        )
        if all_lists:
            the_cards = matching
        else:
            the_cards = [t for t in matching if bool(t.later) == later]
        table = Table(box=SIMPLE, header_style="")
        table.add_column("ID")
        table.add_column("state")
        table.add_column("owner")
        if all_lists:
            table.add_column("list")
        table.add_column("summary")
        for t in the_cards:
            owner = "" if t.owner is None else t.owner
            summary = f"{t.summary} *" if t.details else t.summary
            card_list = ["later" if t.later else "sooner"] if all_lists else []
            table.add_row(str(t.id), t.state, owner, *card_list, summary)
        out = StringIO()
        rich.print(table, file=out)
        print(out.getvalue())
        if any(t.details for t in the_cards):
            print("* has details: cards details ID\n")
        parked = sum(1 for t in matching if t.later)
        if not (later or all_lists) and parked:
            print(f"{parked} more on the Later list: cards list --later\n")


@app.command()
def update(
    card_id: int,
    owner: str = typer.Option(None, "-o", "--owner"),
    summary: List[str] = typer.Option(None, "-s", "--summary"),
):
    """Modify a card in db with given id with new info."""
    summary_str = " ".join(summary) if summary else None
    with cards_db() as db:
        try:
            with_owner_check(
                owner,
                lambda owner: db.update_card(
                    card_id, cards.Card(summary_str, owner, state=None)
                ),
            )
        except cards.InvalidCardId:
            print(f"Error: Invalid card id {card_id}")


@app.command()
def start(card_id: int):
    """Set a card state to 'in prog'."""
    with cards_db() as db:
        try:
            db.start(card_id)
        except cards.InvalidCardId:
            print(f"Error: Invalid card id {card_id}")


@app.command()
def block(card_id: int):
    """Set a card state to 'blocked'."""
    with cards_db() as db:
        try:
            db.block(card_id)
        except cards.InvalidCardId:
            print(f"Error: Invalid card id {card_id}")


@app.command()
def details(
    card_id: int,
    edit: bool = typer.Option(False, "-e", "--edit", help="Edit the details in your $EDITOR."),
):
    """Show a card's details (or edit them with --edit)."""
    with cards_db() as db:
        try:
            card = db.get_card(card_id)
        except cards.InvalidCardId:
            print(f"Error: Invalid card id {card_id}")
            return
        if edit:
            new_details = typer.edit(card.details or "")
            if new_details is None:
                print("No changes.")
                return
            # editors usually add a trailing newline
            db.update_card(card_id, cards.Card(details=new_details.rstrip("\n"), state=None))
            return
        print(f"{card.id}: {card.summary}")
        print()
        print(card.details if card.details else "(no details)")


@app.command()
def finish(card_id: int):
    """Set a card state to 'done'."""
    with cards_db() as db:
        try:
            db.finish(card_id)
        except cards.InvalidCardId:
            print(f"Error: Invalid card id {card_id}")


@app.command("later")
def later_cmd(card_id: int):
    """Move a card to the Later list."""
    with cards_db() as db:
        try:
            db.later(card_id)
        except cards.InvalidCardId:
            print(f"Error: Invalid card id {card_id}")


@app.command()
def sooner(card_id: int):
    """Move a card back to the Sooner list."""
    with cards_db() as db:
        try:
            db.sooner(card_id)
        except cards.InvalidCardId:
            print(f"Error: Invalid card id {card_id}")


@app.command()
def config():
    """List the path to the Cards db."""
    with cards_db() as db:
        print(db.path())


@app.command()
def count():
    """Return number of cards in db."""
    with cards_db() as db:
        print(db.count())


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Cards is a small command line task tracking application.
    """
    if ctx.invoked_subcommand is None:
        list_cards(owner=None, state=None, later=False, all_lists=False)


def get_path():
    db_path_env = os.getenv("CARDS_DB_DIR", "")
    if db_path_env:
        db_path = pathlib.Path(db_path_env)
    else:
        db_path = pathlib.Path.home() / "cards_db"
    return db_path


def open_db():
    """The web app's API if CARDS_URL is set, otherwise the local database."""
    url = os.getenv("CARDS_URL", "")
    if not url:
        return cards.CardsDB(get_path())
    team = os.getenv("CARDS_TEAM", "")
    api_key = os.getenv("CARDS_API_KEY", "")
    if not (team and api_key):
        print("Error: CARDS_URL is set, so CARDS_TEAM and CARDS_API_KEY are needed too.")
        raise typer.Exit(1)
    return RemoteCardsDB(url, team, api_key)


@contextmanager
def cards_db():
    db = open_db()
    try:
        yield db
    except RemoteError as exc:
        print(f"Error: {exc}")
        raise typer.Exit(1)
    finally:
        db.close()


def with_owner_check(owner, func):
    """Call func(owner). If the web app doesn't recognize the owner, ask which
    team member was meant (from its suggestions), and call func again with them."""
    try:
        return func(owner)
    except OwnerNotFound as exc:
        return func(pick_owner(exc))


def pick_owner(exc):
    """Ask which suggested team member was meant; return their email."""
    if len(exc.suggestions) == 1:
        email, name = exc.suggestions[0]
        if typer.confirm(f"'{exc.owner}' isn't a team member. Did you mean {name} ({email})?"):
            return email
        raise typer.Exit(1)
    print(exc.message)
    if not exc.suggestions:
        raise typer.Exit(1)
    for number, (email, name) in enumerate(exc.suggestions, start=1):
        print(f"  {number}: {name} ({email})")
    choice = typer.prompt("Which one? (0 to cancel)", type=int, default=0)
    if 1 <= choice <= len(exc.suggestions):
        return exc.suggestions[choice - 1][0]
    raise typer.Exit(1)


if __name__ == "__main__":
    app()
