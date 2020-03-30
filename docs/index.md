# Welcome to Cards

This is a demo application being built in conjunction with the [Test & Code podcast](http://testandcode.com).

We'll be building up this application, and testing it, and adding functionality, while discussing software testing and development practices.

Follow along, starting with [episode 37](http://testandcode.com/37).

There will be more documentation here at some point. :)


# Usage

See [usage page](usage.md) for details, but here's a demo of how it works:

```
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
```
