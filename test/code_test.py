"""Smoke test."""

from . import u


def test_code():
    t = """
        @code print(2+2)
        @code
            import sys
            print(sys.version)
        @end
    """

    import sys

    s = u.render(t, {})
    assert s.strip() == '4' + sys.version


def test_import():
    t = """
        @import sys, os.path
        >{sys.version}<
        >{os.path.dirname('/foo/bar/baz')}<
    """

    import sys

    s = u.render(t, {})
    assert u.nows(s) == u.nows('>' + sys.version + '<>/foo/bar<')
