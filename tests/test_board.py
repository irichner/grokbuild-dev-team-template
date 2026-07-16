"""Tests for TaskBoard."""

import pytest

from taskboard.board import TaskBoard
from taskboard.models import Task, TaskStatus


def test_add_and_get():
    board = TaskBoard()
    t = board.add("Ship feature", description="do the thing", priority=3)
    assert board.get(t.id) is t
    assert t.title == "Ship feature"
    assert t.priority == 3
    assert t.status == TaskStatus.TODO


def test_add_clamps_priority():
    board = TaskBoard()
    low = board.add("low", priority=-5)
    high = board.add("high", priority=50)
    assert low.priority == 0
    assert high.priority == 10


def test_list_sorted_by_priority_then_title():
    board = TaskBoard()
    board.add("b", priority=1)
    board.add("a", priority=5)
    board.add("c", priority=5)
    titles = [t.title for t in board.list()]
    assert titles == ["a", "c", "b"]


def test_list_filter_status():
    board = TaskBoard()
    t1 = board.add("one")
    t2 = board.add("two")
    board.set_status(t2.id, TaskStatus.DONE)
    assert [t.id for t in board.list(status=TaskStatus.TODO)] == [t1.id]
    assert [t.id for t in board.list(status=TaskStatus.DONE)] == [t2.id]


def test_set_status_unknown():
    board = TaskBoard()
    with pytest.raises(KeyError):
        board.set_status("missing", TaskStatus.DONE)


def test_set_priority_and_remove():
    board = TaskBoard()
    t = board.add("x", priority=1)
    board.set_priority(t.id, 7)
    assert board.get(t.id).priority == 7
    board.remove(t.id)
    assert board.get(t.id) is None
    assert board.count() == 0


def test_set_priority_clamps():
    board = TaskBoard()
    t = board.add("x", priority=5)
    board.set_priority(t.id, -3)
    assert board.get(t.id).priority == 0
    board.set_priority(t.id, 99)
    assert board.get(t.id).priority == 10


def test_set_priority_unknown():
    board = TaskBoard()
    with pytest.raises(KeyError):
        board.set_priority("missing", 3)


def test_get_missing_returns_none():
    board = TaskBoard()
    assert board.get("no-such-id") is None


def test_list_empty_board():
    board = TaskBoard()
    assert board.list() == []


def test_add_empty_title_rejected():
    board = TaskBoard()
    with pytest.raises(ValueError):
        board.add("   ")


def test_list_filter_in_progress():
    board = TaskBoard()
    t = board.add("wip")
    board.set_status(t.id, TaskStatus.IN_PROGRESS)
    assert [x.id for x in board.list(status=TaskStatus.IN_PROGRESS)] == [t.id]


def test_empty_title_rejected():
    with pytest.raises(ValueError):
        Task(title="   ")


def test_remove_unknown():
    board = TaskBoard()
    with pytest.raises(KeyError):
        board.remove("missing")
