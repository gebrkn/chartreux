"""Compiler."""

import u


def test_ERROR_SYNTAX():
    with u.raises_compiler_error('ERROR_SYNTAX'):
        u.render("{1+}")


def test_ERROR_COMMAND():
    with u.raises_compiler_error('ERROR_COMMAND'):
        u.render("@blah")


def test_ERROR_IDENT():
    with u.raises_compiler_error('ERROR_IDENT'):
        u.render("@let $$$")


def test_ERROR_EOF():
    with u.raises_compiler_error('ERROR_EOF'):
        u.render("@if a")


def test_ERROR_DEF():
    with u.raises_compiler_error('ERROR_DEF'):
        u.render("@def ...")


def test_ERROR_FILE():
    with u.raises_compiler_error('ERROR_FILE'):
        u.render("@include bleh")


def test_ERROR_NOT_SUPPORTED():
    with u.raises_compiler_error('ERROR_NOT_SUPPORTED'):
        u.render("{a & b}")


def test_ERROR_FILTER():
    with u.raises_compiler_error('ERROR_FILTER'):
        u.render("{a | 3}")


def test_line_number():
    t = """\
        @each x
        ...
        ...
        @let 123 = ''
        ...
        ...
        @end
    """

    with u.raises_compiler_error('line 4'):
        u.render(t)
