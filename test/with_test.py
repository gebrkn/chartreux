"""WITH command."""

from . import u


def test_with_empty():
    t = """
        >
        @with aa
            yes
        @end
        <
    """

    s = u.render(t, {}, error=u.error)
    assert u.nows(s) == '><'
    assert u.lasterr is None

    s = u.render(t, {'aa': ''}, error=u.error)
    assert u.nows(s) == '><'
    assert u.lasterr is None

    s = u.render(t, {'aa': {}}, error=u.error)
    assert u.nows(s) == '><'
    assert u.lasterr is None


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


def test_with_nested():
    t = """
        >
        @with aa as x
            ({aa.bb.cc})
            ({ERR})
            @with x.bb as y
                ({y.cc})
                ({ERR})
            @end
            ({ERR})
        @end
        ({ERR})
        <
    """
    s = u.render(t, {'aa': {'bb': {'cc': 456}}}, error=u.error)
    assert u.nows(s) == '>(456)()(456)()()()<'
    assert u.lasterr == ('KeyError', '', 12)
