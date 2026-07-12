"""Tests for pure helpers."""

import pytest

from taskboard.util import clamp


def test_clamp_inside_range():
    assert clamp(5, 0, 10) == 5


def test_clamp_below_lo():
    assert clamp(-3, 0, 10) == 0


def test_clamp_above_hi():
    assert clamp(99, 0, 10) == 10


def test_clamp_at_boundaries():
    assert clamp(0, 0, 10) == 0
    assert clamp(10, 0, 10) == 10


def test_clamp_invalid_range():
    with pytest.raises(ValueError, match="lo"):
        clamp(1, 5, 2)
