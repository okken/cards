#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner
import pytest
import pathlib
import cards.cli


@pytest.fixture()
def mock_cards_db(tmpdir, monkeypatch):
    fake_home = pathlib.Path(str(tmpdir.mkdir('fake_home')))
    class FakePathLibPath():
        def home(self):
            return fake_home
    monkeypatch.setattr(cards.cli.pathlib, 'Path', FakePathLibPath)


def test_add(mock_cards_db):
    runner = CliRunner()
    # GIVEN an empty database
    # WHEN a new card is added
    runner.invoke(cards.cli.cards_cli, ['add', 'something'])

    # THEN The listing returns just the new card
    result = runner.invoke(cards.cli.cards_cli, ['list'])
    expected_output = ("  ID      owner  done summary\n"
                       "  --      -----  ---- -------\n"
                       "   1                  something\n")
    assert result.output == expected_output
