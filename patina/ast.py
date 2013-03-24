from patina.utils import FieldReprer
from patina.compiler import Code


class Node(FieldReprer):
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other


class Type(Node):
    def __init__(self, name):
        self.name = name


class Expr(Node):
    def __init__(self, value):
        self.value = value


class Stmt(Expr):
    def compile(self):
        return self.value.compile() + ';'


class Block(Expr):
    def __init__(self, stmts, expr):
        self.stmts = stmts
        self.expr = expr

    def compile(self):
        return Code('{' + ''.join(s.compile() for s in self.stmts) + '}')


class Struct(Stmt):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields


class Fn(Stmt):
    def __init__(self, name, args, returns, block):
        self.name = name
        self.args = args
        self.returns = returns
        self.block = block

    def compile(self):
        return Code('{returns} {name}({args}) {block}'.format(
            name=self.name.name,
            returns=self.returns.name if self.returns else 'void',
            block=self.block.compile(),
            args=', '.join(
                '{0} {1}'.format(field.type, field.name)
                for field in self.args.fields
            )
        ))


class Id(Node):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

    def __repr__(self):
        return 'Id({0})'.format(self.name)


class Field(Node):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class FieldList(Node):
    def __init__(self, fields):
        self.fields = fields


class Literal(Expr):
    def __init__(self, value):
        self.value = value


class Number(Literal):
    def __init__(self, value):
        super(Number, self).__init__(int(value))

    def __eq__(self, other):
        return self.value == other.value


class Array(Literal):
    pass


class String(Literal):
    pass


class Let(Expr):
    def __init__(self, field, expr):
        self.field = field
        self.expr = expr


class If(Expr):
    def __init__(self, condition, then, otherwise):
        self.condition = condition
        self.then = condition
        self.otherwise = otherwise


class Call(Expr):
    def __init__(self, fn, arguments):
        self.fn = fn
        self.arguments = arguments

    def compile(self):
        if self.fn.name == 'print':
            return '''printf("%d", {0})'''.format(self.arguments[0].value)


class BinOp(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    @property
    def value(self):
        return (self.left, self.right)


class Plus(BinOp):
    pass


class Minus(BinOp):
    pass


class Equals(BinOp):
    pass
