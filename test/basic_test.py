"""Smoke test."""

from . import u


def test_render_no_commands():
    t = """aa bb cc dd"""

    s = u.render(t, {})
    assert s == t


def test_empty():
    t = ""

    s = u.render(t, {})
    assert s == t
