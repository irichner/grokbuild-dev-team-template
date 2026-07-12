"""Tests for task tags: normalize, add/remove, and list filter."""

import pytest

from taskboard.board import TaskBoard
from taskboard.models import TaskStatus
from taskboard.util import normalize_tag


# --- normalize_tag ---


def test_normalize_tag_strips_and_lowers():
    assert normalize_tag("  Bug  ") == "bug"
    assert normalize_tag("API") == "api"


def test_normalize_tag_rejects_empty():
    with pytest.raises(ValueError, match="non-empty"):
        normalize_tag("")
    with pytest.raises(ValueError, match="non-empty"):
        normalize_tag("   ")


def test_normalize_tag_rejects_non_str():
    with pytest.raises(TypeError, match="tag must be a str"):
        normalize_tag(None)  # type: ignore[arg-type]


# --- add with tags ---


def test_add_with_tags_normalizes_and_dedupes():
    board = TaskBoard()
    t = board.add("fix", tags=["Bug", "bug", "  api  "])
    assert t.tags == {"bug", "api"}


def test_add_without_tags_defaults_empty():
    board = TaskBoard()
    t = board.add("plain")
    assert t.tags == set()


def test_add_rejects_empty_tag_in_iterable():
    board = TaskBoard()
    with pytest.raises(ValueError, match="non-empty"):
        board.add("bad", tags=["ok", "  "])


# --- add_tag / remove_tag ---


def test_add_tag_and_remove_tag():
    board = TaskBoard()
    t = board.add("work")
    board.add_tag(t.id, "Urgent")
    assert "urgent" in t.tags
    board.remove_tag(t.id, "URGENT")
    assert "urgent" not in t.tags


def test_remove_tag_missing_is_noop():
    board = TaskBoard()
    t = board.add("work", tags=["keep"])
    board.remove_tag(t.id, "absent")
    assert t.tags == {"keep"}


def test_add_tag_unknown_task():
    board = TaskBoard()
    with pytest.raises(KeyError):
        board.add_tag("missing", "bug")


def test_remove_tag_unknown_task():
    board = TaskBoard()
    with pytest.raises(KeyError):
        board.remove_tag("missing", "bug")


def test_add_tag_rejects_empty():
    board = TaskBoard()
    t = board.add("work")
    with pytest.raises(ValueError, match="non-empty"):
        board.add_tag(t.id, "  ")


# --- list filter ---


def test_list_filter_by_tag():
    board = TaskBoard()
    a = board.add("a", tags=["bug"], priority=1)
    board.add("b", tags=["feature"], priority=2)
    c = board.add("c", tags=["bug", "api"], priority=3)
    ids = [t.id for t in board.list(tag="Bug")]
    assert ids == [c.id, a.id]  # sorted by priority desc


def test_list_combined_status_and_tag():
    board = TaskBoard()
    todo_bug = board.add("todo bug", tags=["bug"])
    done_bug = board.add("done bug", tags=["bug"])
    board.add("todo other", tags=["feature"])
    board.set_status(done_bug.id, TaskStatus.DONE)
    result = board.list(status=TaskStatus.TODO, tag="bug")
    assert [t.id for t in result] == [todo_bug.id]


def test_list_tag_filter_normalizes_query():
    board = TaskBoard()
    t = board.add("x", tags=["api"])
    assert board.list(tag="  API  ") == [t]


def test_tags_not_shared_across_tasks():
    """Mutating one task's tags must not affect another (per-task copies)."""
    board = TaskBoard()
    shared = {"seed"}
    a = board.add("a", tags=shared)
    b = board.add("b", tags=shared)
    board.add_tag(a.id, "only-a")
    assert "only-a" in a.tags
    assert "only-a" not in b.tags
    assert "only-a" not in shared
