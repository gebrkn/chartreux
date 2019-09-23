"""Functions."""

from . import u


def test_def():
    t = """
        @def myfun (a, b)
            arg1={a}
            |
            arg2={b}
            |
            {a}/{b}
        @end

        |
        {myfun(x, y)}
        |
        {myfun(u, w)}
        |
    """

    s = u.render(t, {
        'x': 'xx',
        'y': 'yy',
        'u': 'uu',
        'w': 'ww',
    })
    assert u.nows(s) == '|arg1=xx|arg2=yy|xx/yy|arg1=uu|arg2=ww|uu/ww|'


def test_noargs():
    t = """
        @def myfun
            bb
        @end
        |
        {myfun()}
        |
    """

    s = u.render(t)
    assert u.nows(s) == '|bb|'


def test_name_case():
    t = """
        @def myFunAb
            bb
        @end
        |
        {myFunAb()}
        |
        @myFunAb
        |
    """

    s = u.render(t)
    assert u.nows(s) == '|bb|bb|'


def test_sloppy_args():
    t = """
        @def f1 a b
            [ {a}-{b} ]
        @end
        @def f2 a, b
            [ {a}-{b} ]
        @end
        
        {f1('aa', 'bb')}
        {f2('xx', 'yy')}
    """
    s = u.render(t)
    assert u.nows(s) == '[aa-bb][xx-yy]'


def test_default_args():
    t = """
        @def myfun(a, b='DEF')
            [ {a}-{b} ]
        @end
        
        {myfun('aa')}
        {myfun('aa', 'XYZ')}
        {myfun('aa', b='UWV')}
    """
    s = u.render(t)
    assert u.nows(s) == '[aa-DEF][aa-XYZ][aa-UWV]'


def test_star_args():
    t = """
        @def myfun(a, *b)
            [ {a}-{b | join} ]
        @end
        
        {myfun('aa')}
        {myfun('aa', 'X')}
        {myfun('aa', 'X', 'Y')}
    """

    s = u.render(t)
    assert u.nows(s) == '[aa-][aa-X][aa-X,Y]'


def test_2star_args():
    t = """
        @def myfun(a, **b)
            [ {a}-{b | json} ]
        @end
        
        {myfun('aa', p=11, q=22)}
    """

    s = u.render(t)
    assert u.nows(s) == '[aa-{"p":11,"q":22}]'


def test_explicit_return():
    t = """
        @def myfun(a, b)
            @return a + b
        @end

        |
        {myfun(10, 200)}
        |
    """

    s = u.render(t)
    assert u.nows(s) == '|210|'


def test_return_none():
    t = """
        @def myfun(a, b)
            begin
            @if a > b
                @return
            @end
            end
        @end

        |
        {myfun(10, 200)}
        |
        {myfun(1000, 200)}
    """

    s = u.render(t)
    assert u.nows(s) == '|beginend|'


def test_as_command():
    t = """
        @def myfun(a, b)
            {a + b}
        @end

        |
        @myfun 10, 200
        |
        @myfun 10  200
        |
        @myfun (10, 200)
        |
    """

    s = u.render(t)
    assert u.nows(s) == '|210|210|210|'


def test_as_command_with_keyword_args():
    t = """
        @def myfun(a, b)
            {a + b}
        @end
        |
        @myfun a=10, b=200
        |
    """

    s = u.render(t)
    assert u.nows(s) == '|210|'


def test_as_filter():
    t = """
        @def myfun(a, b=200)
            {a + b}
        @end

        |
        {aa | myfun}
        |
        {aa | myfun(300)}
        |
    """
    d = {'aa': 5}
    s = u.render(t, d)
    assert u.nows(s) == '|205|305|'


def test_block():
    t = """
        @block myblock(text, a, b)
            {a} {text} {b}
        @end

        @myblock '>', '<'
            some
            text
        @end
    """
    s = u.render(t)
    assert u.nows(s) == '>sometext<'


def test_scope():
    t = '''
        @let c = 'C'
        
        @def use():
            [ {a},{b},{c} ]
        @end

        @def overwrite(b):
            @let c = 'newC'
            [ {a},{b},{c} ]
        @end
        
        [ {a},{b},{c}] 
        {use()}
        {overwrite('newB')}
    '''

    d = {'a': 'A', 'b': 'B'}
    s = u.render(t, d)
    assert u.nows(s) == '[A,B,C][A,B,C][A,newB,newC]'


def test_dynamic_scope():
    t = '''
        @let c = 0
        @let d = 0
        
        @def use():
            [ {a},{b},{c} ]
        @end

        @def overwrite(b):
            @let c = 'newC'
            [ {a},{b},{c} ]
        @end
        
        @let c = 'C'
        
        [ {a},{b},{c}] 
        {use()}
        {overwrite('newB')}
    '''

    d = {'a': 'A', 'b': 'B'}
    s = u.render(t, d)
    assert u.nows(s) == '[A,B,C][A,B,C][A,newB,newC]'
