"""Smoke test."""

import u


def test():
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
