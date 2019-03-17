"""Silent mode."""

import u

def test_no_var():
    t = """
        >{aa}<
    """
    d = {}
    err = []

    s = u.render(t, {}, warn=err.append, silent=True)
    assert len(err) == 1
    assert u.nows(s) == '><'

    with u.raises_template_error('KeyError'):
        u.render(t, {}, silent=False)


def test_no_key():
    t = """
        >{aa.bb}<
    """

    d = {'aa': 123}
    err = []

    s = u.render(t, d, warn=err.append, silent=True)
    assert len(err) == 1
    assert u.nows(s) == '><'

    with u.raises_template_error('AttributeError'):
        u.render(t, d, silent=False)


def test_no_prop():
    t = """
        >{aa.bb}<
    """

    d = {'aa': {}}
    err = []

    s = u.render(t, d, warn=err.append, silent=True)
    assert len(err) == 1
    assert u.nows(s) == '><'

    with u.raises_template_error('AttributeError'):
        u.render(t, d, silent=False)


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

    s = u.render(t, d, warn=err.append, silent=True)
    assert len(err) == 1
    assert u.nows(s) == '><'

    with u.raises_template_error('TypeError'):
        u.render(t, d, silent=False)


def test_exceptions():
    t = """
        ZeroDivisionError: [ {1/0} ]
        KeyError: [ {foobar} ]
        TypeError: [ {aa()} ]
    """

    d = {'aa': 1}
    err = []

    s = u.render(t, d, warn=err.append, silent=True)
    assert len(err) == 3
    assert u.nows(s) == 'ZeroDivisionError:[]KeyError:[]TypeError:[]'

    with u.raises_template_error('ZeroDivisionError'):
        u.render(t, d, silent=False)
