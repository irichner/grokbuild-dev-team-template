"""CLI smoke tests."""

from taskboard.cli import main


def test_add_prints_task(capsys):
    assert main(["add", "Hello", "--priority", "2"]) == 0
    out = capsys.readouterr().out
    assert "Hello" in out
    assert "p=2" in out


def test_list_empty(capsys):
    assert main(["list"]) == 0


def test_done_missing(capsys):
    assert main(["done", "no-such-id"]) == 1
    err = capsys.readouterr().err
    assert "not found" in err


def test_add_with_description(capsys):
    assert main(["add", "T", "--description", "d"]) == 0
    assert "T" in capsys.readouterr().out
