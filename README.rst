=====
cards
=====


.. image:: https://img.shields.io/pypi/v/cards.svg
        :target: https://pypi.python.org/pypi/cards

.. image:: https://img.shields.io/travis/okken/cards.svg
        :target: https://travis-ci.org/okken/cards

.. image:: https://ci.appveyor.com/api/projects/status/hk18x9ovqv3d7kpw?svg=true
    :target: https://ci.appveyor.com/project/okken/cards

.. image:: https://readthedocs.org/projects/cards-project/badge/?version=latest
        :target: https://cards-project.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://codecov.io/gh/okken/cards/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/okken/cards

Project task tracking / todo list

This is a demo application being built in conjunction with
the `Test & Code podcast <http://testandcode.com>`__.

We'll be building up this application, and testing it, and adding
functionality, while discussing software testing and development
practices.

Follow along, starting with `episode 37 <http://testandcode.com/37>`__.


* Free software: MIT license
* Documentation: https://cards-project.readthedocs.io.


Usage
-----

See usage_ page for details, but here's a demo of how it works::

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


.. _usage: https://cards-project.readthedocs.io/en/latest/usage/

