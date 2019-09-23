"""Error handling."""

from . import u


def test_no_var():
    t = """
        >{aa}<
    """

    s = u.render(t, {}, error=u.error, path='xyz')
    assert u.lasterr == ('KeyError', 'xyz', 2)
    assert u.nows(s) == '><'

    with u.raises_template_error(KeyError):
        u.render(t, {})


def test_no_key():
    t = """
        foo
        >{aa.bb}<
    """

    d = {'aa': 123}
    err = []

    s = u.render(t, d, error=u.error, path='xyz')
    assert u.lasterr == ('AttributeError', 'xyz', 3)
    assert u.nows(s) == 'foo><'

    with u.raises_template_error(AttributeError):
        u.render(t, d)


def test_no_prop():
    t = """\
        >{aa.bb}<
    """

    d = {'aa': {}}

    s = u.render(t, d, error=u.error, path='xyz')
    assert u.lasterr == ('AttributeError', 'xyz', 1)
    assert u.nows(s) == '><'

    with u.raises_template_error(AttributeError):
        u.render(t, d)


def test_no_iterable():
    t = """
        >
        @each aa
            ...
        @end
        <
    """

    d = {'aa': 123}
    err = []

    s = u.render(t, d, error=u.error, path='xyz')
    assert u.lasterr == ('TypeError', 'xyz', 3)
    assert u.nows(s) == '><'

    with u.raises_template_error(TypeError):
        u.render(t, d)


def test_code():
    t = """
        foo
        >{1/0}<
        bar
    """

    d = {'aa': 1}

    s = u.render(t, d, error=u.error, path='xyz')
    assert u.lasterr == ('ZeroDivisionError', 'xyz', 3)

    assert u.nows(s) == 'foo><bar'

    with u.raises_template_error(ZeroDivisionError):
        u.render(t, d)
