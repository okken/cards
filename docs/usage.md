Usage
=====

Cards is implemented as a command line application.

Preconditions
-------------

If cards is installed (with `python setup.py install`) you may use it from your command line.

Console Help
-------------
To invoke the usage on the commandline call `cards --help` 
Here is the output from the version 0.1.5:

```
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

To get help on the commands options and arguements use `cards [command] --help`

**NOTE:** *The details of the commands will not be listed here but described in the following sections*

Basic Actions
-------------

| Action                | Commandline    |
|-----------------------|----------------|
| add a card            | `cards add "name of the task in strings"` |
| show your cards       | `cards list` |
| delete a card         | `cards [id]` |
| show your cards       | `cards count` |

Options 
---------

The following options are supported by some of the commands 

| Options                    | Description |
|----------------------------|-----------------------------|
| -o/--owner [NAME]         | add a owner named NAME    |
| -s/--summary [TASK]       | set a (new) summary       |
| -d/--done [BOOL]          | mark a task state true/1=done (marked with x) false/0=open |

**NOTE:** *The add command will not support the `--summary` option, but use the positional argument*
