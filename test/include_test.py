"""@include command."""

from . import u


def test_include(tmpdir):
    tmpdir.join('t1').write('T-1')
    tmpdir.mkdir('sub1').join('a').write('SUB-1-A')
    tmpdir.mkdir('sub2').join('b').write('SUB-2-B')

    main = tmpdir.join('sub2', 'c')
    main.write("""
            SUB-2-C
            |
            @include ../sub1/a
            |
            @include ../t1
            |
            @include b
    """)

    s = u.render_path(main.strpath)
    assert u.nows(s) == 'SUB-2-C|SUB-1-A|T-1|SUB-2-B'


def test_include_errors(tmpdir):
    tmpdir.join('defs').write('''
        *
        @def foo x
            <{42//x}>
        @end
        *
    ''')
    main = tmpdir.join('uses')
    main.write('''
        2
        @include defs
        4
        @foo 1
        @foo 0
        7
    ''')

    s = u.render_path(main.strpath, error=u.error, silent=True)
    assert u.lasterr == ('ZeroDivisionError', 'defs', 4)
    assert u.nows(s) == '2**4<42><>7'
