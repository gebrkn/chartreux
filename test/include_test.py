"""@include command."""

import u


def test_include():
    u.tempfile('t1', 'T-1')
    u.tempfile('sub1/a', 'SUB-1-A')
    u.tempfile('sub2/b', 'SUB-2-B')

    main = u.tempfile('sub2/c', """
            SUB-2-C
            |
            @include ../sub1/a
            |
            @include ../t1
            |
            @include b
    """)

    s = u.render_path(main)
    assert u.nows(s) == 'SUB-2-C|SUB-1-A|T-1|SUB-2-B'
