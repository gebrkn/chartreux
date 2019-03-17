"""WITH command."""

import u


def test_with_empty():
    t = """
        >
        @with aa
            yes
        @end
        <
    """

    s = u.render(t, {})
    assert u.nows(s) == '><'

    s = u.render(t, {'aa': ''})
    assert u.nows(s) == '><'

    s = u.render(t, {'aa': {}})
    assert u.nows(s) == '><'


def test_with_not_empty():
    t = """
        >
        @with aa
            yes
        @end
        <
    """

    s = u.render(t, {'aa': 1})
    assert u.nows(s) == '>yes<'

    s = u.render(t, {'aa': 0})
    assert u.nows(s) == '>yes<'


def test_with_ref():
    t = """
        >
        @with aa as x
            {x.bb}
        @end
        <
    """
    s = u.render(t, {'aa': {'bb': 456}})
    assert u.nows(s) == '>456<'
