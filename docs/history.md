History
=======

0.2.9 (2020-04-03)
------------------
- version bump to test CD

0.2.6 (2020-03-30)
------------------
- setuptools -> flit
- click -> typer
- pre-commit
- black
- flake8

0.2.4 (2019-03-08)
------------------
- README.rst -> README.md

0.2.2 (2019-03-06)
------------------
- add priority

0.2.1 (2019-02-28)
------------------
- rewrote API, tests

0.1.12 (2018-04-26)
------------------
- list now supports --format and accepts all formats that the tabulate package
formats.
- uses dataclass insead of attrs for Python 3.7

0.1.11 (2018-03-28)
------------------
- restructure to use src dir
- more thourogh testing for filter

0.1.10 (2018-03-23)
------------------
- add filtering to list command
- thank you Felix Häberle for starting this work

0.1.9 (2018-03-21)
------------------
- remove coveralls.io (version 0.1.9)
- add coveralls.io (version 0.1.8)

0.1.7 (2018-03-20)
------------------
- unpeg dependencies

0.1.6 (2018-03-20)
------------------
- automate the 1 manual test in both cli and api versions
- mark tracer bullet tests with pytest.mark.smoke
- mark cli tests with pytest.mark.cli
- mark alac tests with pytest.mark.alac
- add coverage to tox runs
- add smoketest and alactest targets to Makefile

0.1.5 (2018-03-16)
------------------
- (internal) change version version handling in `setup.py` to read it from `cards/__init__.py`
- (internal) take out versions from requirements_dev.txt
- (internal) refacter tests directory into cli and cardsdb directories
- (internal) finish tracer bullet tests for both API and CLI

0.1.4 (2018-03-09)
------------------

-   Cleaning up extra files, cleaning up Makefile, and setup.py.
-   Had to bump version to test "make release"

0.1.3 (2018-03-09)
------------------

-   Running cards with no command now runs list instead of help.

0.1.2 (2018-03-07)
------------------

-   Add CLI tests

0.1.1 (2018-03-06)
------------------

-   Add rudimentary functionality

0.1.0 (2018-03-05)
------------------

-   First release on PyPI. This is just from the cookie cutter template.
-   There is no functionality available yet.
