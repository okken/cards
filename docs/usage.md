Usage
=====

Cards is implemented as a command line application.

Console Help
-------------
To invoke the usage on the commandline call `cards --help`
Here is the output from the version 0.1.10:

```
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
```

To get help on the commands options and arguements use `cards [command] --help`.

Here are a few...

Adding a card
-------------

```
$ cards add --help
Usage: cards add [OPTIONS] SUMMARY

  add a card

Options:
  -o, --owner TEXT  set the card owner
  -h, --help        Show this message and exit.
```

Listing cards
-------------

```
cards list --help
Usage: cards list [OPTIONS]

  list cards

Options:
  -n, --noowner       filter on the card without owners
  -o, --owner TEXT    filter on the card owner
  -d, --done BOOLEAN  filter on cards with given done state
  -f, --format TEXT   table formatting option, eg. "grid", "simple", "html"
  -h, --help          Show this message and exit.
```

Updating a card
---------------

```
$ cards update --help
Usage: cards update [OPTIONS] CARD_ID

  update card

Options:
  -o, --owner TEXT    change the card owner
  -s, --summary TEXT  change the card summary
  -d, --done BOOLEAN  change the card done state (True or False)
  -h, --help          Show this message and exit.
```


Basic Actions
-------------

| Action                | Commandline    |
|-----------------------|----------------|
| add a card            | `cards add "name of the task in strings"` |
| show your cards       | `cards list` |
| delete a card         | `cards delete [id]` |
| count your cards      | `cards count` |

Options
---------

The following options are supported by some of the commands

| Options                    | Description |
|----------------------------|-----------------------------|
| -o/--owner [NAME]         | add a owner named NAME    |
| -s/--summary [TASK]       | set a (new) summary       |
| -d/--done [BOOL]          | mark a task state true/1=done (marked with x) false/0=open |

**NOTE:** *The add command will not support the `--summary` option, but use the positional argument*
