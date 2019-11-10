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


def test_strip():
    t = '{2+2} xxx {3+3} yyy {4+4}'

    s = u.render(t)
    assert s == '4 xxx 6 yyy 8'

    s = u.render(t, strip=True)
    assert s == '4xxx6yyy8'
