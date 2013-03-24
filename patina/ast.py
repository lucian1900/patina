class Node(object):
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        ast_fields = [
            str(k) + '=' + repr(v)
            for k, v in self.__dict__.iteritems()
            if '_' not in k and not hasattr(v, '__call__')
        ]

        return self.__class__.__name__ + '(' + ', '.join(ast_fields) + ')'


class Expr(Node):
    def __init__(self, value):
        self.value = value


class Stmt(Expr):
    pass


class Block(Expr):
    def __init__(self, stmts, expr):
        self.stmts = stmts
        self.expr = expr


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


class Id(Node):
    def __init__(self, name):
        self.name = name

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
