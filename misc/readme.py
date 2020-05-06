import sys
import os
import re

DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(DIR + '/..'))

import chartreux


def _example(m):
    delim = '---'
    t = [x.strip() for x in m.group(1).split(delim)]

    tpl = t[0]
    ctx = t[1] if len(t) > 1 else None

    res = chartreux.render(tpl, eval(ctx) if ctx else None).rstrip()

    res = re.sub(r'^( *\n)+', '', res.rstrip())

    out = []

    qq = '```'
    hh = '###### '

    out.extend([hh + 'example:', qq, tpl, qq])

    if ctx:
        out.extend([hh + 'context:', qq, ctx, qq])

    out.extend([hh + 'result:', qq, res, qq])

    return '\n'.join(out)


def _process(text):
    text = re.sub(r'(?s)```EXAMPLE(.+?)```', _example, text)

    toc = []

    for ln in text.splitlines():
        m = re.match(r'^(#{2,4})( .+)', ln.strip())
        if m:
            d, t = m.groups()
            toc.append(
                '%s * [%s](#%s)' % (
                    '    ' * (len(d) - 2),
                    t.strip(),
                    t.strip().lower().replace(' ', '-')
                ))

    text = text.replace('{toc}', '\n'.join(toc))
    return text


with open(DIR + '/README.src.md') as fp:
    text = fp.read()

with open(DIR + '/../README.md', 'w') as fp:
    fp.write(_process(text))
