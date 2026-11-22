cards
=====

Project task tracking / todo list

A Teaching Project
----------------------------

This project is used for teaching the concepts of software testing.
Specifically, testing with the pytest test framework.

The project appears in:
- [The Complete pytest Course](https://courses.pythontest.com/)
  - uses cards version 2.0.0: `pip install cards==2.0.0`
- [Python Testing with pytest, 2nd edition](https://pythontest.com/pytest-book/)
  - uses cards version 1.0.1 - approximately: `pip install cards==1.0.1`

Version 3 adds features for using cards as a real task tracker, including the
[Cards web app](https://cards.pythontest.com). If you're following the course or the
book, install the version above, so the code and output match.

Installing
----------

    pip install cards

or, to keep it in its own environment:

    uv tool install cards

Can be used as a simple todo list
---------------------------------

Even though the primary goal of the project is for teaching about software testing, I also use it as a simple command line task tracker for myself and my team.

Usage
-----

Here's a demo of how it works:

    $ cards add a todo
    $ cards add -o Brian another task
    $ cards list

    ID   state   owner   summary
    ───────────────────────────────────
    1    todo            a todo
    2    todo    Brian   another task

    $ cards update 1 -o Brian
 .  $ cards
                                     
    ID   state   owner   summary       
    ─────────────────────────────────── 
      1    todo    Brian   a todo        
      2    todo    Brian   another task  
                                      
    $ cards start 1
    $ cards
                                       
      ID   state     owner   summary       
     ───────────────────────────────────── 
      1    in prog   Brian   a todo        
      2    todo      Brian   another task 

    $ cards finish 1
    $ cards

      ID   state   owner   summary
     ───────────────────────────────────
      2    todo    Brian   another task

Done cards are hidden unless you ask for them:

    $ cards list -s all

      ID   state   owner   summary
     ───────────────────────────────────
      1    done    Brian   a todo
      2    todo    Brian   another task

    $ cards block 2
    $ cards details 2 --edit    # or add a card with details: cards add -d ...
    $ cards

      ID   state     owner   summary
     ─────────────────────────────────────────
      2    blocked   Brian   another task *

    * has details: cards details ID

    $ cards details 2
    2: another task

    Waiting on a reply from Anna.

    $ cards delete 1
    Delete card 1: a todo? [y/N]: y
    $ cards list -s all

      ID   state     owner   summary
     ─────────────────────────────────────────
      2    blocked   Brian   another task *

    * has details: cards details ID

Cards you're not getting to soon can be parked on the Later list.
`cards` and `cards list` show the Sooner list, and mention how many cards are waiting:

    $ cards add rewrite the docs --later
    $ cards

      ID   state     owner   summary
     ─────────────────────────────────────────
      2    blocked   Brian   another task *

    * has details: cards details ID

    1 more on the Later list: cards list --later

    $ cards list --later

      ID   state   owner   summary
     ───────────────────────────────────────
      3    todo            rewrite the docs

    $ cards sooner 3      # move it back; `cards later ID` parks a card
    $ cards list --all    # both lists, with a "list" column

    $ cards --help

     Usage: cards [OPTIONS] COMMAND [ARGS]...

     Cards is a small command line task tracking application.

    ╭─ Options ────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                      │
    ╰──────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────╮
    │ add       Add a card to db.                                      │
    │ block     Set a card state to 'blocked'.                         │
    │ config    List the path to the Cards db.                         │
    │ count     Return number of cards in db.                          │
    │ delete    Remove card in db with given id (asks first).          │
    │ details   Show a card's details (or edit them with --edit).      │
    │ finish    Set a card state to 'done'.                            │
    │ later     Move a card to the Later list.                         │
    │ list      List open cards (use -s all to include done ones) on   │
    │           the Sooner list (or --later, or --all).                │
    │ projects  List the team's projects, or add one (web app only).   │
    │ sooner    Move a card back to the Sooner list.                   │
    │ start     Set a card state to 'in prog'.                         │
    │ update    Modify a card in db with given id with new info.       │
    │ version   Return version of cards application                    │
    ╰──────────────────────────────────────────────────────────────────╯


Using the Cards web app
-----------------------

By default, cards are stored in a local file (`~/cards_db`, or `CARDS_DB_DIR`).

To use a team's cards on the Cards web app instead, set:

    export CARDS_URL=https://cards.pythontest.com
    export CARDS_TEAM=<team slug, as in /a/<team slug>/ in web app URLs>
    export CARDS_API_KEY=<an API key from your profile page in the web app>

The commands work the same way. `cards config` shows which web app and team
you're using. Owners are team members: use `-o me`, or a member's email or
name. If an owner doesn't match anyone on the team, cards asks who you meant:

    $ cards add fix the docs -o brain
    'brain' isn't a team member. Did you mean Brian Okken? [y/N]: y

### Projects

On the web app, a team can have several projects, each with its own Sooner and
Later lists. Card numbers are unique across the team, so commands that act on one
card, like `cards start 42`, work whatever project the card is in.

Listing and adding use the team's default project, unless you pick one with
`CARDS_PROJECT` or `-p` (which wins):

    $ export CARDS_PROJECT=website     # e.g. per code repo, with direnv
    $ cards                            # the website project's open cards
    $ cards add -p docs fix the typos  # add to another project
    $ cards list -p all                # every project, with a project column
    $ cards update 42 -p docs          # move a card to another project
    $ cards projects                   # the team's projects and open card counts
    $ cards projects add docs          # add a project

Projects are managed on the web app's Projects page too. They don't exist for
local-file cards.
