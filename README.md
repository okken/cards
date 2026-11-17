cards
=====

Project task tracking / todo list

A Teaching Project
----------------------------

This project is used for teaching the concepts of software testing.
Specifically, testing with the pytest test framework.

The project appears in:
- [The Complete pytest Course](https://courses.pythontest.com/)
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
      1    done    Brian   a todo
      2    todo    Brian   another task


    $ cards block 2
    $ cards details 2 --edit
    $ cards

      ID   state     owner   summary
     ─────────────────────────────────────────
      1    done      Brian   a todo
      2    blocked   Brian   another task *

    * has details: cards details ID

    $ cards details 2
    2: another task

    Waiting on a reply from Anna.

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
    │ block     Set a card state to 'blocked'.                         │
    │ config    List the path to the Cards db.                         │
    │ count     Return number of cards in db.                          │
    │ delete    Remove card in db with given id.                       │
    │ details   Show a card's details (or edit them with --edit).      │
    │ finish    Set a card state to 'done'.                            │
    │ list      List cards in db.                                      │
    │ start     Set a card state to 'in prog'.                         │
    │ update    Modify a card in db with given id with new info.       │
    │ version   Return version of cards application                    │
    ╰──────────────────────────────────────────────────────────────────╯


Using the Cards web app
-----------------------

By default, cards are stored in a local file (`~/cards_db`, or `CARDS_DB_DIR`).

To use a team's cards on the Cards web app instead, set:

    export CARDS_URL=https://<cards web app address>
    export CARDS_TEAM=<team slug, as in /a/<team slug>/ in web app URLs>
    export CARDS_API_KEY=<an API key from your profile page in the web app>

The commands work the same way. `cards config` shows which web app and team
you're using. Owners are team members: use `-o me`, or a member's email or
name. If an owner doesn't match anyone on the team, cards asks who you meant:

    $ cards add fix the docs -o brain
    'brain' isn't a team member. Did you mean Brian Okken (brian@pythontest.com)? [y/N]: y
