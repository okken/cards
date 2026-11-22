# Changelog

All notable changes to this project will be documented in this file.

<!--

TEMPLATE EXAMPLE ONLY.
DO NOT EDIT ANYTHING BETWEEN TEMPLATE_START AND TEMPLATE_END.

TEMPLATE_START

## [UNRELEASED_TEMPLATE_EXAMPLE] - yyyy-month-dd

### Highlights

- nothing so far

### Migration Notes

- nothing so far

### Added

- nothing so far

### Changed

- nothing so far

### Deprecated

- nothing so far

### Removed

- nothing so far

### Fixed

- nothing so far

### Developer Experience

- nothing so far

TEMPLATE_END

-->

## [3.0.0] - 22-Nov-2026

### Highlights

- Cards can now use the [Cards web app](https://cards.pythontest.com) as its database, so a team
  shares one list from the command line and the browser.
- New for everyone: a Later list, a "blocked" state, card details, and done cards hidden by default.
- The pytest course and book use earlier versions. Install those with `pip install cards==2.0.0`
  (course) or `pip install cards==1.0.1` (book).

### Migration Notes

- `cards` and `cards list` no longer show done cards. Use `cards list -s all` to see them.
- `cards delete N` now asks before deleting. Use `-y` / `--yes` in scripts.
- Existing local databases (`~/cards_db`) work as they are.

### Added

- Optional web app mode: when `CARDS_URL` is set (with `CARDS_TEAM` and
  `CARDS_API_KEY`), the CLI stores cards in the Cards web app through its API
  instead of the local database. Local mode is unchanged.
- In web app mode, an owner that doesn't match a team member gets a
  "Did you mean ...?" prompt, using the web app's suggestions.
- Projects (web app mode only): `CARDS_PROJECT`, `-p` on `add`, `list` and `update`,
  `cards list -p all`, and `cards projects` / `cards projects add`.
- A Later list: `cards later N`, `cards sooner N`, `cards add --later`, and
  `cards list --later` / `--all`. `cards list` says how many cards are on the Later list.
- A "blocked" state: `cards block N`.
- Card details: `cards details N` shows them, `cards details N --edit` edits them in
  `$EDITOR`, and `cards add -d` writes them when adding. Cards with details are marked `*`
  in lists.

### Changed

- `cards list` hides done cards; `-s all` shows every state.
- `cards delete N` shows the card and asks before deleting it. Use `-y` / `--yes`
  to skip the question.

## [2.0.2] - 24-Oct-2026

### Developer Experience

- Add a changelog.
- Update Readme
    - Include "start" example.
    - Fix link to course

## [2.0.0] - 9-Sept-2023

### Highlights

- Version of cards used in [The Complete pytest Course](https://courses.pythontest.com/).

### Migration Notes

- Requires Python 3.8 or newer (previously Python 3.7 or newer).

### Changed

- Update the TinyDB, Typer, and Rich dependencies.
- Modernize API type annotations; the existing task-tracking commands remain available.

### Developer Experience

- Reorganize API and CLI tests into command-focused test modules.
- Add support for running the CLI as `python -m cards.cli`.

## [1.0.1] - 12-June-2022


- Approximate version of cards used in [Python Testing with pytest, 2nd edition](https://pythontest.com/pytest-book/)