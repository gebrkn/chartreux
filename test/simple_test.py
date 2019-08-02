"""Simple commands."""

from . import u



def test_quote():
    t = """
        >
        @quote abc
            @if 123
            @end
            xyz
        @end abc
        <
    """
    s = u.render(t)
    assert u.nows(s) == '>@if123@endxyz<'


def test_let_expr():
    t = """
        @let myvar (2+2) * 3
        >{myvar}<
    """
    s = u.render(t)
    assert u.nows(s) == '>12<'


def test_let_block():
    t = """
        @let myvar 
            abc
            def
        @end
        >{myvar}<
    """
    s = u.render(t)
    assert u.nows(s) == '>abcdef<'


def test_nested_let_block():
    t = """
        @let aa
            abc
            @let bb
                uwv
            @end
            def
        @end
        >{aa}<
        >{bb}<

    """
    s = u.render(t)
    assert u.nows(s) == '>abcdef<>uwv<'
