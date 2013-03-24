from patina.utils import FieldReprer


class InferenceError(Exception):
    pass


class Node(FieldReprer):
    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self == other


class Type(Node):
    def __init__(self, name):
        self.name = name

    def compile(self, ctx):
        return self.name


class Expr(Node):
    type = None

    def __init__(self, value):
        self.value = value
        self.type = None


class Stmt(Expr):
    def compile(self, ctx):
        return self.value.compile(ctx) + '; '


class Block(Expr):
    def __init__(self, stmts, expr):
        self.stmts = stmts
        self.expr = expr

    def compile(self, ctx):
        return '{' + ''.join(i.compile(ctx) for i in self.stmts) + '}'

    @property
    def type(self):
        return self.expr.type if self.expr else None


class Struct(Stmt):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields

    def compile(self, ctx):
        return


class Fn(Stmt):
    def __init__(self, name, args, returns, block):
        self.name = name
        self.args = args
        self.returns = returns
        self.block = block

    def compile(self, ctx):
        return '{returns} {name}({args}) {block}'.format(
            name=self.name.compile(ctx),
            returns=self.returns.compile(ctx) if self.returns else 'void',
            block=self.block.compile(ctx),
            args=self.args.compile(ctx)
        )


class Id(Expr):
    def __init__(self, name):
        self.name = name

    def compile(self, ctx):
        return self.name


class Field(Node):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def compile(self, ctx):
        return self.name.compile(ctx) + ' ' + self.type.compile(ctx)


class FieldList(Node):
    def __init__(self, fields):
        self.fields = fields

    def compile(self, ctx):
        return ', '.join(i.compile(ctx) for i in self.fields)


class Literal(Expr):
    def __init__(self, value):
        self.value = value


class Number(Literal):
    type = Type('int')

    def __init__(self, value):
        super(Number, self).__init__(int(value))

    def __eq__(self, other):
        return self.value == other.value

    def compile(self, ctx):
        return str(self.value)


class Array(Literal):
    pass


class String(Literal):
    pass


class Let(Expr):
    def __init__(self, field, expr):
        self.field = field
        self.expr = expr

    @property
    def type(self):
        if self.field.type is not None:
            return self.field.type

        if self.expr.type:
            return self.expr.type

        raise InferenceError("Can't infer type for " + repr(self))


class If(Expr):
    def __init__(self, condition, then, otherwise):
        self.condition = condition
        self.then = then
        self.otherwise = otherwise

    def compile(self, ctx):
        return '{cond} ? {then} : {other}'.format(
            cond=self.condition.compile(ctx),
            then=self.then.compile(ctx),
            other=self.otherwise.compile(ctx),
        )


class Call(Expr):
    def __init__(self, fn, arguments):
        self.fn = fn
        self.arguments = arguments

    def compile(self, ctx):
        if self.fn.name == 'print':
            return 'printf("%d", {0})'.format(self.arguments[0].value)

        return self.fn.name.compile(ctx) + '(' + self.arguments.compile(ctx) + ')'

    @property
    def type(self):
        return self.fn.returns


class Ns(Node):
    def __init__(self, types, fns):
        self.types = types
        self.fns = fns
