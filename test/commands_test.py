"""Custom commands."""

from . import u



def test_commands():

    class T:
        def command_foo(self, cc, arg):
            cc.code.add(f'print("[[" + {arg} + "]]")')
        def command_bar(self, cc, arg):
            cc.code.add('_PUSHBUF()')
            cc.parser.parse_until('end')
            cc.code.add(f'print("<" + _POPBUF() + "><" + {arg} + ">")')

    t = '''
        @foo "123"
        @bar "456"
            789
        @end
        
    '''

    s = u.render(t, commands=T())
    assert u.nows(s) == '[[123]]<789><456>'
