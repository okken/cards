cards
=====

Project task tracking / todo list

A Teaching Project
----------------------------

This project is used for teaching the concepts of software testing.
Specifically, testing with the pytest test framework.

The project appears in:
- [The Complete pytest Course](https://pythontest.com/courses/)
  - uses cards version 2.0.0
- [Python Testing with pytest, 2nd edition](https://pythontest.com/pytest-book/)
  - uses cards version 1.0.1 - approximately

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


    $ cards finish 1
    $ cards

      ID   state   owner   summary
     ───────────────────────────────────
      1    done    Brian   a todo
      2    todo    Brian   another task


    $ cards delete 1
    $ cards

      ID   state   owner   summary
     ───────────────────────────────────
      2    todo    Brian   another task

    $ cards --help

     Usage: cards [OPTIONS] COMMAND [ARGS]...

     Cards is a small command line task tracking application.

    ╭─ Options ────────────────────────────────────────────────────────╮
    │ --help          Show this message and exit.                      │
    ╰──────────────────────────────────────────────────────────────────╯
    ╭─ Commands ───────────────────────────────────────────────────────╮
    │ add       Add a card to db.                                      │
    │ config    List the path to the Cards db.                         │
    │ count     Return number of cards in db.                          │
    │ delete    Remove card in db with given id.                       │
    │ finish    Set a card state to 'done'.                            │
    │ list      List cards in db.                                      │
    │ start     Set a card state to 'in prog'.                         │
    │ update    Modify a card in db with given id with new info.       │
    │ version   Return version of cards application                    │
    ╰──────────────────────────────────────────────────────────────────╯
