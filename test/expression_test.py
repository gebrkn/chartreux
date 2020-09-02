"""String interpolation."""

from . import u


def test_simple_property():
    t = '>{aa}<'
    d = {'aa': 123}
    s = u.render(t, d)
    assert s == '>123<'


def test_no_parse_with_default_delims():
    t = '''{ no parse }>{aa}<'''
    d = {'aa': 123}
    s = u.render(t, d)
    assert s == '{ no parse }>123<'


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


def test_operators():
    t = '''
        [ {aa.x + bb.y * 4} ]
        [ {cc.z in [1,2,3]} ]
        [ {cc.z not in [4,5,6]} ]
        [ {3 < dd.w < 5} ]
        
    '''
    d = {'aa': {'x': 2}, 'bb': {'y': 10}, 'cc': {'z': 1}, 'dd': {'w': 4}}
    s = u.render(t, d)
    assert u.nows(s) == '[42][True][True][True]'


def test_if():
    t = '''
        [ {'yes' if aa else 'no'} ]
        [ {'yes' if bb else 'no'} ]
        
    '''
    d = {'aa': True, 'bb': False}
    s = u.render(t, d)
    assert u.nows(s) == '[yes][no]'


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


def test_explicit_var():
    t = '>{_["foo bar"].boo}<'
    d = {'foo bar': {'boo': 123}}
    s = u.render(t, d)
    assert s == '>123<'
