cards
=====

[![image](https://img.shields.io/pypi/v/cards.svg)](https://pypi.python.org/pypi/cards)
[![image](https://github.com/okken/cards/workflows/CI/badge.svg?branch=master)](https://github.com/okken/cards/actions?workflow=CI)
[![Documentation Status](https://readthedocs.org/projects/cards-project/badge/?version=latest)](https://cards-project.readthedocs.io/en/latest/?badge=latest)
[![image](https://codecov.io/gh/okken/cards/branch/master/graph/badge.svg)](https://codecov.io/gh/okken/cards)

Project task tracking / todo list

Initial Goals of the project
----------------------------

-   Create a command line application that can be used to track the
    status of a multi-person project.
-   Explore the problems inherent in all applications regarding
    usability, testing, packaging, deployment, etc.

Rough Current Status
--------------------

-   A \"usable\" API and CLI.
-   Database location is flexible to the API, but the CLI hard codes it
    to a single user home directory.

Usage
-----

See [usage](https://cards-project.readthedocs.io/en/latest/usage/) page
for details, but here\'s a demo of how it works:

    $ cards add a todo

    $ cards add -o Brian another task

    $ cards list
         ╷       ╷       ╷
      ID │ state │ owner │ summary
    ╺━━━━┿━━━━━━━┿━━━━━━━┿━━━━━━━━━━━━━━╸
      1  │ todo  │       │ a todo
      2  │ todo  │ Brian │ another task
         ╵       ╵       ╵

    $ cards update 1 -o Brian

    $ cards finish 1

    $ cards
      ID │ state │ owner │ summary
    ╺━━━━┿━━━━━━━┿━━━━━━━┿━━━━━━━━━━━━━━╸
      1  │ done  │ Brian │ a todo
      2  │ todo  │ Brian │ another task
         ╵       ╵       ╵

    $ cards delete 1

    $ cards
      ID │ state │ owner │ summary
    ╺━━━━┿━━━━━━━┿━━━━━━━┿━━━━━━━━━━━━━━╸
      2  │ todo  │ Brian │ another task
         ╵       ╵       ╵

    $ cards --help
    Usage: cards [OPTIONS] COMMAND [ARGS]...

      Cards is a small command line task tracking application.

    Options:
      --help  Show this message and exit.

    Commands:
      add      Add a card to db.
      config   List the path to the Cards db.
      count    Return number of cards in db.
      delete   Remove card in db with given id.
      finish   Set a card state to 'done'.
      list     List cards in db.
      start    Set a card state to 'in prog'.
      update   Modify a card in db with given id with new info.
      version  Return version of cards application

