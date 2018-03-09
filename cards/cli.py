"""Command Line Interface (CLI) for cards project."""

import click
import cards
import pathlib


@click.group(invoke_without_command=True,
             context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(version=cards.__version__)
@click.pass_context
def cards_cli(ctx):
    """Run the cards application."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(list_cards)


@cards_cli.command(help="add a card")
@click.argument('summary')
@click.option('-o', '--owner', default=None,
              help='set the card owner')
def add(summary, owner):
    """Add a card to db."""
    cards_db().add(cards.Card(summary, owner))


@cards_cli.command(help="delete a card")
@click.argument('card_id', type=int)
def delete(card_id):
    """Remove card in db with given id."""
    cards_db().delete(card_id)


@cards_cli.command(name="list", help="list cards")
def list_cards():
    """
    List cards in db.

    If owner given, only list cards with that owner.
    """
    formatstr = "{: >4} {: >10} {: >5} {}"
    print(formatstr.format('ID', 'owner', 'done', 'summary'))
    print(formatstr.format('--', '-----', '----', '-------'))
    for t in cards_db().list_cards():
        done = ' x ' if t.done else ''
        owner = '' if t.owner is None else t.owner
        print(formatstr.format(
              t.id, owner, done, t.summary))


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
    cards_db().update(card_id, cards.Card(summary, owner, done))


@cards_cli.command(help="list count")
def count():
    """Return number of cards in db."""
    print(cards_db().count())


def cards_db():
    # just put it in users home dir for now
    db_path = pathlib.Path().home() / '.cards_db.json'
    return cards.CardsDB(db_path)


if __name__ == '__main__':
    cards_cli()
