import json

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalTrueColorFormatter

def ppd(d, indent=None):
    'pretty-prints a dict'
    print(highlight(
        code      = json.dumps(d, indent=indent),
        lexer     = JsonLexer(),
        formatter = TerminalTrueColorFormatter()
    ).strip())
