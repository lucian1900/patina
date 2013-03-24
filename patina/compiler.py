import subprocess


class Code(str):
    cc = 'cc'

    def compile(self):
        subprocess.call(['cc', '-x', 'c', '-'], self)


class CompilerContext(object):
    def __init__(self):
        self.types = {}
        self.fns = {}


def compile(ast):
    ctx = CompilerContext()

    return ast.compile(ctx)
