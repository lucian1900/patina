class Node(object):
    pass


class Expr(Node):
    def __init__(self, value):
        self.value = value


class BinOp(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Plus(BinOp):
    pass


class Minus(BinOp):
    pass


class Times(BinOp):
    pass


class Divide(BinOp):
    pass
