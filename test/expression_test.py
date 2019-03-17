"""String interpolation."""

import u


def test_simple_property():
    t = '>{aa}<'
    d = {'aa': 123}
    s = u.render(t, d)
    assert s == '>123<'


def test_nested_property():
    t = '>{aa["bb"][0]["cc"]}<'
    d = {'aa': {'bb': [{'cc': 123}]}}
    s = u.render(t, d)
    assert s == '>123<'


def test_nested_property_dot_notation():
    t = '>{aa.bb[0].cc}<'
    d = {'aa': {'bb': [{'cc': 123}]}}
    s = u.render(t, d)
    assert s == '>123<'


def test_nested_object():
    class C:
        xx = {'yy': 'zz'}

    t = '>{aa.bb.xx.yy}<'
    d = {'aa': {'bb': C()}}
    s = u.render(t, d)
    assert s == '>zz<'


def test_methods():
    t = '''
        @each aa.values() as v
            [ {v} ]
        @end
    '''
    d = {'aa': {'a': 1, 'b': 2, 'c': 3}}
    s = u.render(t, d)
    assert u.nows(s) == '[1][2][3]'


def test_local_var():
    t = '''
        [{aa.bb}]
        [{xx}]

        @let aa {'bb': 'new'}
        @let xx 'new2'

        [{aa.bb}]
        [{xx}]
    '''

    d = {'aa': {'bb': 'old'}, 'xx': 'old2'}
    s = u.render(t, d)
    assert u.nows(s) == '[old][old2][new][new2]'


def test_built_in_name():
    t = '>{abs.__name__}{len("hello")}<'
    d = {}
    s = u.render(t, d)
    assert s == '>abs5<'


import sys


def test_var():
    t = '''
        @var sys
        @code import sys
        >{sys.version}<
    '''
    d = {}
    s = u.render(t, d)
    assert s.strip() == '>' + sys.version + '<'


def test_var2():
    t = '''
        @var k
        @code 
            class K:
                val = 123
                d = {'p': 'q'}
            k = K()
        @end
        
        >{k.val}<>{k.d.p}<
    '''
    d = {}
    s = u.render(t, d)
    assert s.strip() == '>123<>q<'
