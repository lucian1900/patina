class Node(object):
    def __eq__(self, other):
        return self.value == other.value


class Expr(Node):
    def __init__(self, value):
        self.value = value


class Literal(Expr):
    pass


class Number(Literal):
    def __init__(self, value):
        self.value = int(value)


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
