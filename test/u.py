import re
import sys
import os
import time
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + '/../chartreux')

import chartreux


def dump(text, **opts):
    print('-' * 40)
    print(chartreux.translate(text, **opts))
    print('-' * 40)


def render(src, context=None, **opts):
    return chartreux.render(src, context, **opts)


def render_path(path, context=None, **opts):
    return chartreux.render_path(path, context, **opts)


def nows(s):
    return re.sub(r'\s+', '', s.strip())


def raises_template_error(exc):
    return pytest.raises(exc)


def raises_compiler_error(msg):
    return pytest.raises(chartreux.compiler.Error, match=msg)


lasterr = None


def error(exc, path, line):
    global lasterr
    if path:
        path = os.path.basename(path)
    lasterr = exc.__class__.__name__, path, line
