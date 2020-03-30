cards
=====

[![image](https://img.shields.io/pypi/v/cards.svg)](https://pypi.python.org/pypi/cards)
[![image](https://github.com/okken/cards/workflows/CI/badge.svg?branch=master)](https://github.com/okken/cards/actions?workflow=CI)
[![Documentation Status](https://readthedocs.org/projects/cards-project/badge/?version=latest)](https://cards-project.readthedocs.io/en/latest/?badge=latest)
[![image](https://codecov.io/gh/okken/cards/branch/master/graph/badge.svg)](https://codecov.io/gh/okken/cards)

Project task tracking / todo list (in progress)

Initial Goals of the project
----------------------------

-   Create a command line application that can be used to track the
    status of a multi-person project.
-   Explore the problems inherent in all applications regarding
    usability, testing, packaging, deployment, etc.

Rough Current Status
--------------------

-   A \"usable\" API and CLI. The CLI workflow needs work.
-   Database location is flexible to the API, but the CLI hardcodes it
    to a single user home directory.

More info
---------

This is a demo application being built in conjunction with the [Test &
Code podcast](http://testandcode.com).

We\'ll be building up this application, and testing it, and adding
functionality, while discussing software testing and development
practices.

Follow along, starting with [episode 37](http://testandcode.com/37).

-   Free software: MIT license
-   Documentation: <https://cards-project.readthedocs.io>.

Usage
-----

See [usage](https://cards-project.readthedocs.io/en/latest/usage/) page
for details, but here\'s a demo of how it works:

    $ cards add 'a todo'

    $ cards add -o Brian 'another task'

    $ cards list
      ID      owner  done summary
      --      -----  ---- -------
       1                  a todo
       2      Brian       another task

    $ cards update 1 -o Brian

    $ cards update 1 --done True

    $ cards
      ID      owner  done summary
      --      -----  ---- -------
       1      Brian    x  a todo
       2      Brian       another task

    $ cards delete 1

    $ cards
      ID      owner  done summary
      --      -----  ---- -------
       2      Brian       another task

    $ cards --help
    Usage: cards [OPTIONS] COMMAND [ARGS]...

      Run the cards application.

    Options:
      --version   Show the version and exit.
      -h, --help  Show this message and exit.

    Commands:
      add     add a card
      count   list count
      delete  delete a card
      list    list cards
      update  update card
