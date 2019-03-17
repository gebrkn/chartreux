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
    return chartreux.render_text(src, context, **opts)


def render_path(path, context=None, **opts):
    return chartreux.render_path(path, context, **opts)


def nows(s):
    return re.sub(r'\s+', '', s.strip())


_temp_dir = '/tmp/chartreux' + str(int(time.time()))


def tempfile(path, text):
    path = os.path.join(_temp_dir, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wt') as fp:
        fp.write(text)
    return path


def raises_template_error(msg):
    return pytest.raises(chartreux.runtime.Error, match=msg)


def raises_compiler_error(msg):
    return pytest.raises(chartreux.compiler.Error, match=msg)
