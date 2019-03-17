"""IF command."""

import u


def test_if():
    t = """
        @if aa > 1
            yes
        @end
    """
    s = u.render(t, {'aa': 0})
    assert u.nows(s) == ''
    s = u.render(t, {'aa': 2})
    assert u.nows(s) == 'yes'


def test_if_else():
    t = """
        @if aa > 1
            yes
        @else
            no
        @end
    """
    s = u.render(t, {'aa': 2})
    assert u.nows(s) == 'yes'
    s = u.render(t, {'aa': 0})
    assert u.nows(s) == 'no'


def test_if_elif():
    t = """
        @if aa > 10
            >10
        @elif aa > 5
            >5
        @else
            <=5
        @end
    """
    s = u.render(t, {'aa': 20})
    assert u.nows(s) == '>10'
    s = u.render(t, {'aa': 8})
    assert u.nows(s) == '>5'
    s = u.render(t, {'aa': 4})
    assert u.nows(s) == '<=5'


def test_nested_if():
    t = """
        @if aa > 5
            >5
            @if aa > 10
                >10
                @if aa > 20
                    >20
                @end
            @else
                <10
            @end
        @elif aa > 2
            >2
        @else
            <=2
            @if aa > 1
                =2
            @else
                =1
            @end
        @end
    """
    s = u.render(t, {'aa': 25})
    assert u.nows(s) == '>5>10>20'

    s = u.render(t, {'aa': 15})
    assert u.nows(s) == '>5>10'

    s = u.render(t, {'aa': 5})
    assert u.nows(s) == '>2'

    s = u.render(t, {'aa': 2})
    assert u.nows(s) == '<=2=2'

    s = u.render(t, {'aa': 1})
    assert u.nows(s) == '<=2=1'
