"""Filters."""

import u


def test_filter_raw():
    t = '>{aa | raw}<'
    d = {'aa': 'bb'}
    s = u.render(t, d)
    assert s == '>bb<'


def test_filter_as_int():
    t = '>{aa | as_int}<'
    d = {'aa': '0000099'}
    s = u.render(t, d)
    assert s == '>99<'


def test_filter_as_float():
    t = '>{aa | as_float}<'
    d = {'aa': '0000099.770000'}
    s = u.render(t, d)
    assert s == '>99.77<'


def test_filter_as_str():
    t = '>{aa | as_str}<'
    d = {'aa': 123}
    s = u.render(t, d)
    assert s == '>123<'


def test_filter_html():
    t = '>{aa | html}<'
    d = {'aa': '<b>'}
    s = u.render(t, d)
    assert s == '>&lt;b&gt;<'


def test_filter_nl2br():
    t = '>{aa | nl2br}<'
    d = {'aa': 'aa\nbb'}
    s = u.render(t, d)
    assert s == '>aa<br/>bb<'


def test_filter_strip():
    t = '>{aa | strip}<'
    d = {'aa': '  123  '}
    s = u.render(t, d)
    assert s == '>123<'


def test_filter_upper():
    t = '>{aa | upper}<'
    d = {'aa': 'abcDEF'}
    s = u.render(t, d)
    assert s == '>ABCDEF<'


def test_filter_lower():
    t = '>{aa | lower}<'
    d = {'aa': 'abcDEF'}
    s = u.render(t, d)
    assert s == '>abcdef<'


def test_filter_linkify():
    t = '>{aa | linkify}<'
    d = {'aa': 'abc https://www.com def'}
    s = u.render(t, d)
    assert s == '>abc <a href="https://www.com">https://www.com</a> def<'


def test_filter_unhtml():
    t = '>{aa | unhtml}<'
    d = {'aa': '<b> abc &lt;b&gt;'}
    s = u.render(t, d)
    assert s == '><b> abc <b><'


def test_filter_format():
    t = '>{aa | format("{:03d}")}<'
    d = {'aa': 7}
    s = u.render(t, d)
    assert s == '>007<'


def test_filter_cut():
    t = '>{aa | cut(3)}<'
    d = {'aa': '0123456'}
    s = u.render(t, d)
    assert s == '>012<'


def test_filter_slice():
    t = '>{aa | slice(1, 4)}<'
    d = {'aa': '0123456'}
    s = u.render(t, d)
    assert s == '>123<'


def test_filter_json():
    class C:
        def __init__(self):
            self.aa = 'füßchen'
            self.bb = 'yy'

    t = '>{aa | json}<'
    d = {'aa': {'cc': C()}}
    s = u.render(t, d)
    assert s == r'>{"cc": {"aa": "f\u00fc\u00dfchen", "bb": "yy"}}<'


def test_format_filter():
    t = '>{aa | "{:.2f}"},{aa | ":.2f"}<'
    d = {'aa': '123'}
    s = u.render(t, d)
    assert s == '>123.00,123.00<'


def test_combined_filters():
    t = '>{aa | upper | html | "!r"}<'
    d = {'aa': '<b>A'}
    s = u.render(t, d)
    assert s == ">'&lt;B&gt;A'<"


def test_default_filter():
    t = '>{aa}<'
    d = {'aa': '<b>A'}
    s = u.render(t, d, filter='html')
    assert s == '>&lt;b&gt;A<'
