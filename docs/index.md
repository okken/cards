# Welcome to Cards

This project may be useful on its own. However, the main intent is as an example project to discuss testing practices.

# Usage

```
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
```
