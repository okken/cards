"""Command Line Interface (CLI) for cards project."""
import os
from io import StringIO
import pathlib
import rich
from rich.table import Table
from rich.box import SIMPLE
from contextlib import contextmanager
from datetime import datetime
from enum import Enum
from typing import List, Optional

import cards
from cards.remote import OwnerNotFound, RemoteCardsDB, RemoteError

import typer

app = typer.Typer(add_completion=False)


class Priority(str, Enum):
    high = "high"
    normal = "normal"
    low = "low"


PRIORITY_HELP = "high, normal or low. High cards are listed first, low ones last."


@app.command()
def version():
    """Return version of cards application"""
    print(cards.__version__)


@app.command()
def add(
    summary: List[str],
    owner: str = typer.Option(None, "-o", "--owner"),
    project: Optional[str] = typer.Option(
        None, "-p", "--project", help="A project's name (web app only). Defaults to CARDS_PROJECT."
    ),
    later: bool = typer.Option(False, "-l", "--later", help="Put the card on the Later list."),
    priority: Optional[Priority] = typer.Option(None, "-P", "--priority", help=PRIORITY_HELP),
    with_details: bool = typer.Option(
        False, "-d", "--details", help="Write the card's details in your $EDITOR."
    ),
):
    """Add a card to db."""
    summary_str = " ".join(summary) if summary else None
    details = None
    if with_details:
        # None if the editor is closed without saving; editors usually add a trailing newline
        details = (typer.edit("") or "").rstrip("\n") or None
    with cards_db(project) as db:
        with_owner_check(
            owner,
            lambda owner: db.add_card(
                cards.Card(
                    summary_str,
                    owner,
                    state="todo",
                    details=details,
                    later=later or None,
                    priority=priority.value if priority and priority != Priority.normal else None,
                )
            ),
        )


@app.command()
def delete(
    card_id: int,
    yes: bool = typer.Option(False, "-y", "--yes", help="Delete without asking first."),
):
    """Remove card in db with given id (asks first)."""
    with cards_db() as db:
        try:
            card = db.get_card(card_id)
            if not yes and not typer.confirm(f"Delete card {card_id}: {card.summary}?"):
                print("Not deleted.")
                return
            db.delete_card(card_id)
        except cards.InvalidCardId:
            print(f"Error: Invalid card id {card_id}")


@app.command("list")
def list_cards(
    owner: Optional[str] = typer.Option(None, "-o", "--owner"),
    state: str = typer.Option(
        "open",
        "-s",
        "--state",
        help="open (everything but done), all, todo, in prog, paused or done.",
    ),
    later: bool = typer.Option(False, "-l", "--later", help="Show the Later list."),
    all_lists: bool = typer.Option(False, "-a", "--all", help="Show both the Sooner and Later lists."),
    project: Optional[str] = typer.Option(
        None,
        "-p",
        "--project",
        help="A project's name, or all (web app only). Defaults to CARDS_PROJECT.",
    ),
):
    """
    List open cards (use -s all to include done ones) on the Sooner list (or --later, or --all).
    """
    with cards_db(project) as db:
        db_state = None if state in ("open", "all") else state
        matching = with_owner_check(
            owner, lambda owner: db.list_cards(owner=owner, state=db_state)
        )
        if state == "open":
            matching = [t for t in matching if t.state != "done"]
        if all_lists:
            the_cards = matching
        else:
            the_cards = [t for t in matching if bool(t.later) == later]
        the_cards = sorted(the_cards, key=cards.Card.sort_key)
        show_priority = any(t.priority for t in the_cards)
        listed_project = getattr(db, "listed_project", None)
        all_projects = isinstance(db, RemoteCardsDB) and listed_project is None
        if listed_project:
            print(f"Project: {listed_project}")
        table = Table(box=SIMPLE, header_style="")
        table.add_column("ID")
        table.add_column("state")
        if show_priority:
            table.add_column("priority")
        table.add_column("owner")
        if all_projects:
            table.add_column("project")
        if all_lists:
            table.add_column("list")
        table.add_column("summary")
        for t in the_cards:
            owner = "" if t.owner is None else t.owner
            summary = f"{t.summary} *" if t.details else t.summary
            extra = [t.project or ""] if all_projects else []
            if all_lists:
                extra.append("later" if t.later else "sooner")
            priority = [t.priority or ""] if show_priority else []
            table.add_row(str(t.id), t.state, *priority, owner, *extra, summary)
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
    project: Optional[str] = typer.Option(
        None, "-p", "--project", help="Move the card to this project (web app only)."
    ),
    priority: Optional[Priority] = typer.Option(None, "-P", "--priority", help=PRIORITY_HELP),
):
    """Modify a card in db with given id with new info."""
    summary_str = " ".join(summary) if summary else None
    with cards_db(project) as db:
        try:
            with_owner_check(
                owner,
                lambda owner: db.update_card(
                    card_id,
                    cards.Card(
                        summary_str,
                        owner,
                        state=None,
                        project=project,
                        priority=priority.value if priority else None,
                    ),
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
def pause(card_id: int):
    """Set a card state to 'paused'."""
    with cards_db() as db:
        try:
            db.pause(card_id)
        except cards.InvalidCardId:
            print(f"Error: Invalid card id {card_id}")


# The old name for pause, before 3.1. Hidden, so it doesn't clutter --help.
app.command("block", hidden=True)(pause)


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
        comments = db.list_comments(card_id) if isinstance(db, RemoteCardsDB) else []
        if comments:
            print()
            print("Comments:")
            for c in comments:
                author = c["author"]["name"] if c.get("author") else "Someone"
                print()
                print(f"  {author}, {local_time(c['created_at'])}:")
                for line in c["text"].splitlines():
                    print(f"    {line}")


@app.command()
def comment(card_id: int, text: List[str]):
    """Add a comment to a card (web app only)."""
    with cards_db() as db:
        require_web_app(db, "comments")
        try:
            db.add_comment(card_id, " ".join(text))
        except cards.InvalidCardId:
            print(f"Error: Invalid card id {card_id}")


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


projects_app = typer.Typer(help="List the team's projects, or add one (web app only).")
app.add_typer(projects_app, name="projects")


@projects_app.callback(invoke_without_command=True)
def projects(ctx: typer.Context):
    """List the team's projects (web app only)."""
    if ctx.invoked_subcommand is not None:
        return
    with cards_db() as db:
        require_web_app(db)
        current = os.getenv("CARDS_PROJECT", "")
        table = Table(box=SIMPLE, header_style="")
        table.add_column("project")
        table.add_column("open cards", justify="right")
        table.add_column("")
        for p in db.list_projects():
            notes = []
            if p["is_default"]:
                notes.append("default")
            if current and p["name"].lower() == current.lower():
                notes.append("CARDS_PROJECT")
            table.add_row(p["name"], str(p["open_cards"]), ", ".join(notes))
        out = StringIO()
        rich.print(table, file=out)
        print(out.getvalue())


@projects_app.command("add")
def projects_add(name: List[str]):
    """Add a project to the team."""
    with cards_db() as db:
        require_web_app(db)
        db.add_project(" ".join(name))


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
        list_cards(owner=None, state="open", later=False, all_lists=False, project=None)


def get_path():
    db_path_env = os.getenv("CARDS_DB_DIR", "")
    if db_path_env:
        db_path = pathlib.Path(db_path_env)
    else:
        db_path = pathlib.Path.home() / "cards_db"
    return db_path


def open_db(project=None):
    """The web app's API if CARDS_URL is set, otherwise the local database.

    `project` (from -p) overrides CARDS_PROJECT; projects only exist in the web app.
    """
    url = os.getenv("CARDS_URL", "")
    if not url:
        if project:
            print("Error: projects need the web app (set CARDS_URL).")
            raise typer.Exit(1)
        return cards.CardsDB(get_path())
    team = os.getenv("CARDS_TEAM", "")
    api_key = os.getenv("CARDS_API_KEY", "")
    if not (team and api_key):
        print("Error: CARDS_URL is set, so CARDS_TEAM and CARDS_API_KEY are needed too.")
        raise typer.Exit(1)
    return RemoteCardsDB(url, team, api_key, project=project or os.getenv("CARDS_PROJECT") or None)


def local_time(iso: str) -> str:
    """An API timestamp (UTC) as local time, to the minute."""
    # Python 3.10's fromisoformat doesn't accept the "Z" (UTC) suffix the API uses.
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone().strftime("%Y-%m-%d %H:%M")


def require_web_app(db, feature="projects"):
    if not isinstance(db, RemoteCardsDB):
        print(f"Error: {feature} need the web app (set CARDS_URL).")
        raise typer.Exit(1)


@contextmanager
def cards_db(project=None):
    db = open_db(project)
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
