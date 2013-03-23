class Node(object):
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other


class Expr(Node):
    def __init__(self, value):
        self.value = value


class Group(Expr):
    pass


class Statement(Expr):
    pass


class Block(Node):
    def __init__(self, exprs):
        self.exprs = exprs


class Id(Expr):
    pass
    #def __eq__(self, other):
    #    return self.value == other.value


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
    def __init__(self, name, type, expr):
        self.name = name
        self.type = type
        self.expr = expr


class If(Expr):
    def __init__(self, condition, then, otherwise):
        self.condition = condition
        self.then = condition
        self.otherwise = otherwise


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
