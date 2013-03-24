from __future__ import print_function
import sys
import subprocess

from patina.parser import parse


def main():
    code = ''
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            code = f.read()

    elif len(sys.argv) == 3 and sys.argv[1] == '-c':
        code = sys.argv[2]

    else:
        print('Error: Wrong arguments')
        return

    try:
        ast = parse(code)
    except ValueError as e:
        print('Syntax error: ' + e.message)
        return

    c = ast.compile()
    print(c)

    pipe = subprocess.Popen(['cc', '-x', 'c', '-'], stdin=subprocess.PIPE)
    pipe.communicate(input=c)
