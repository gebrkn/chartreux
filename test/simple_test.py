"""Simple commands."""

from . import u


def test_quote():
    t = """
        >
        @quote abc
            @if 123
            {foo}
            @end
            xyz
        @end abc
        <
    """
    s = u.render(t)
    assert u.nows(s) == '>@if123{foo}@endxyz<'


def test_quote_no_label():
    t = """
        >
        @quote
            {foo}
        @end
        <
    """
    s = u.render(t)
    assert u.nows(s) == '>{foo}<'


def test_comment():
    t = """
        >
        @comment abc
            @if 123
            {foo}
            @end
            xyz
        @end abc
        <
    """
    s = u.render(t)
    assert u.nows(s) == '><'


def test_comment_no_label():
    t = """
        >
        @comment
            {foo}
        @end
        <
    """
    s = u.render(t)
    assert u.nows(s) == '><'


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


def test_multi_let_vars():
    t = """
        @let aa,bb  , cc abc
        >{aa}<
        >{bb}<
        >{cc}<

    """
    d = {'abc': 'ABC'}
    s = u.render(t, d)
    assert u.nows(s) == '>A<>B<>C<'
