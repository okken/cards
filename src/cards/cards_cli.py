"""Command Line Interface (CLI) for cards project."""

import os
import click
import cards
import json
from tabulate import tabulate

DEFAULT_TABLEFORMAT = os.environ.get('CARDSTABLEFORMAT', 'simple')


@click.group(invoke_without_command=True,
             context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version=cards.__version__)
@click.pass_context
def cards_cli(ctx):
    """Run the cards application."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(list_cards, noowner=None, owner=None, done=None)


@cards_cli.command(help="add a card")
@click.argument('summary', nargs=-1)
@click.option('-o', '--owner', default=None,
              help='set the card owner')
def add(summary, owner):
    """Add a card to db."""
    cards.set_db_path()
    summary = ' '.join(summary)
    cards.add_card(cards.Card(summary, owner))


@cards_cli.command(help="delete a card")
@click.argument('card_id', type=int)
def delete(card_id):
    """Remove card in db with given id."""
    cards.set_db_path()
    cards.delete_card(card_id)


@cards_cli.command(name="list", help="list cards")
@click.option('-n', '--noowner', default=None, is_flag=True,
              help='filter on the card without owners')
@click.option('-o', '--owner', default=None,
              help='filter on the card owner')
@click.option('-d', '--done', default=None,
              type=bool,
              help='filter on cards with given done state')
@click.option('-f', '--format', default=DEFAULT_TABLEFORMAT,
              type=str,
              help='table formatting option, eg. "grid", "simple", "html"')
def list_cards(noowner, owner, done, format):
    """
    List cards in db.
    """
    cards.set_db_path()
    filter = {'noowner': noowner, 'owner': owner, 'done': done}
    the_cards = cards.list_cards(filter=filter)

    #  json is a special case
    if format == 'json':
        items = [c.to_dict() for c in the_cards]
        print(json.dumps({"cards": items}, sort_keys=True, indent=4))
        return

    # who's going to remember 'pipe' for markdown?
    if format == 'markdown':
        format = 'pipe'

    if format == 'packed':
        for t in the_cards:
            done = 'x' if t.done else 'o'
            owner = 'unassigned' if t.owner is None else t.owner
            line = f'{t.id} {owner} {done} {t.summary}'
            print(line)
        return

    # all formats except json/none use tabulate
    items = []
    for t in the_cards:
        done = ' x ' if t.done else ''
        owner = '' if t.owner is None else t.owner
        items.append((t.id, owner, done, t.summary))

    print(tabulate(items,
                   headers=('ID', 'owner', 'done', 'summary'),
                   tablefmt=format))


@cards_cli.command(help="mark card as done")
@click.argument('card_id', type=int)
def finish(card_id):
    """Modify a card in db with given id with new info."""
    cards.set_db_path()
    cards.update_card(card_id, cards.Card(done=True))


@cards_cli.command(help="update card")
@click.argument('card_id', type=int)
@click.option('-o', '--owner', default=None,
              help='change the card owner')
@click.option('-s', '--summary', default=None,
              help='change the card summary')
@click.option('-d', '--done', default=None,
              type=bool,
              help='change the card done state (True or False)')
def update(card_id, owner, summary, done):
    """Modify a card in db with given id with new info."""
    cards.set_db_path()
    cards.update_card(card_id, cards.Card(summary, owner, done))



@cards_cli.command(help="list count")
@click.option('-n', '--noowner', default=None, is_flag=True,
              help='count cards without owners')
@click.option('-o', '--owner', default=None,
              help='count cards with given owner')
@click.option('-d', '--done', default=None,
              type=bool,
              help='count cards with given done state')
def count(noowner, owner, done):
    """Return number of cards in db."""
    cards.set_db_path()
    print(cards.count(noowner, owner, done))

