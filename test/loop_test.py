"""EACH command."""

import u


def test_nokey():
    t = """
        @each it
            *
        @end
    """
    d = {'it': ['aaa', 'bbb', 'ccc']}
    s = u.render(t, d)
    assert u.nows(s) == '***'


def test_value():
    t = """
        @each it as e
            {e}!
        @end
    """
    d = {'it': ['aaa', 'bbb', 'ccc']}
    s = u.render(t, d)
    assert u.nows(s) == 'aaa!bbb!ccc!'


def test_key_value():
    t = """
        @each it as n, e
            {n}={e}!
        @end
    """
    d = {'it': ['aaa', 'bbb', 'ccc']}
    s = u.render(t, d)
    assert u.nows(s) == '0=aaa!1=bbb!2=ccc!'


def test_index():
    t = """
        @each it index k
            {k}!
        @end
    """
    d = {'it': ['aaa', 'bbb', 'ccc']}
    s = u.render(t, d)
    assert u.nows(s) == '1!2!3!'


def test_index_len():
    t = """
        @each it index k, total
            {k}-{total}!
        @end
    """
    d = {'it': ['aaa', 'bbb', 'ccc']}
    s = u.render(t, d)
    assert u.nows(s) == '1-3!2-3!3-3!'


def test_value_index():
    t = """
        @each it as e index k
            {k}={e}!
        @end
    """
    d = {'it': ['aaa', 'bbb', 'ccc']}
    s = u.render(t, d)
    assert u.nows(s) == '1=aaa!2=bbb!3=ccc!'


def test_dict_value():
    t = """
        @each it as key, val
            {key}={val}!
        @end
    """
    d = {'it': {'a': 'aaa', 'c': 'ccc', 'b': 'bbb'}}
    s = u.render(t, d)
    assert u.nows(s) == 'a=aaa!c=ccc!b=bbb!'


def test_empty():
    t = """
        >
        @each it as e
            {e}
        @end
        <
    """
    d = {'it': []}
    s = u.render(t, d)
    assert u.nows(s) == '><'


def test_empty_else():
    t = """
        >
        @each it as e
            {e}
        @else
            EMPTY!
        @end
        <
    """
    d = {'it': []}
    s = u.render(t, d)
    assert u.nows(s) == '>EMPTY!<'
