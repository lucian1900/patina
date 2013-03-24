from functools import wraps

from rply import ParserGenerator

from patina.lexer import lexer
from patina.ast import *


pg = ParserGenerator(
    [rule.name for rule in lexer.rules],
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', 'EQUALS'),
    ],
    cache_id='patina',
)


def applied(f):
    @wraps(f)
    def wrapper(args):
        return f(*args)


@pg.production('main : expr')
@pg.production('main : stmt')
@pg.production('main : decl')
@pg.production('main : ns')
def main(p):
    return p[0]


@pg.production('id : ID')
def identifier(p):
    return Id(p[0].getstr())


@pg.production('type : COLON ID')
def type_(p):
    return Type(p[1].getstr())


@pg.production('type :')
def type_empty(p):
    pass


@pg.production('opttype :')
def opttype_empty(p):
    pass


@pg.production('opttype : type')
def opttype(p):
    return p[0]


@pg.production('field : id type')
def field_typed(p):
    name, type = p
    return Field(name, type)


@pg.production('inferredfield : id opttype')
def inferred_field_typed(p):
    name, type = p
    return Field(name, type)


@pg.production('exprlist :')
@pg.production('exprlist : expr')
@pg.production('exprlist : exprlist COMMA expr')
@pg.production('structlist :')
@pg.production('structlist : struct')
@pg.production('structlist : structlist SEMI struct')
@pg.production('decllist :')
@pg.production('decllist : decl')
@pg.production('decllist : decllist decl')
@pg.production('fnlist :')
@pg.production('fnlist : fn')
@pg.production('fnlist : fnlist SEMI fn')
@pg.production('arglist :')
@pg.production('arglist : field')
@pg.production('arglist : arglist COMMA field')
@pg.production('fieldlist : field')
@pg.production('fieldlist : fieldlist COMMA field')
@pg.production('stmtlist : stmt')
@pg.production('stmtlist : stmtlist stmt')
def prodlist(p):
    if len(p) == 0:
        return []

    elif len(p) == 1:
        i = p[0]
        if i is None:
            return []
        return [i]

    elif len(p) == 2:
        lst, i = p
        return lst + [i]

    else:
        lst, _, i = p
        return lst + [i]


@pg.production('expr : id')
def identifier_expr(p):
    return p[0]


@pg.production('expr : LPAREN expr RPAREN')
def group(p):
    _, expr, _ = p
    return expr


@pg.production('stmt : expr SEMI')
def stmt(p):
    expr, _ = p
    return Stmt(expr)


@pg.production('block :')
def block_empty(p):
    pass


@pg.production('block : LBRACE expr RBRACE')
def block_single(p):
    _, expr, _ = p
    return Block([], expr)


@pg.production('block : LBRACE stmtlist expr RBRACE')
def block(p):
    _, stmts, expr, _ = p
    return Block(stmts, expr)


@pg.production('block : LBRACE stmtlist RBRACE')
def block_stmt(p):
    _, stmts, _ = p
    return Block(stmts, None)


@pg.production('expr : block')
def block_expr(p):
    return p[0]


@pg.production('let : LET inferredfield ASSIGN expr')
def let(p):
    _,  field, _, expr = p
    return Let(field, expr)


@pg.production('expr : let')
def let_expr(p):
    return p[0]


@pg.production('expr : IF expr block')
def if_(p):
    _, condition, then = p
    return If(condition, then, None)


@pg.production('expr : IF expr block ELSE block')
def if_else(p):
    _, condition, then, _, otherwise = p
    return If(condition, then, otherwise)


@pg.production('struct : STRUCT id LBRACE fieldlist RBRACE')
def struct(p):
    _, name, _, fields, _ = p
    return Struct(name, fields)


@pg.production('decl : struct')
def struct_stmt(p):
    return p[0]


@pg.production('fn : FN id LPAREN arglist RPAREN RETURNS id block')
def fn_returns(p):
    _, name, _, fields, _, _, returns, block = p
    return Fn(name, fields, returns, block)


@pg.production('fn : FN id LPAREN arglist RPAREN block')
def fn(p):
    _, name, _, fields, _, block = p
    return Fn(name, fields, None, block)


@pg.production('decl : fn')
def fn_stmt(p):
    return p[0]


# Literals
@pg.production('expr : NUMBER')
def literal(p):
    return Number(p[0].getstr())


# Array
@pg.production('expr : LBRACKET exprlist RBRACKET')
def array(p):
    _, exprs, _ = p
    return Array(exprs or [])


# Call
@pg.production('expr : id LPAREN exprlist RPAREN')
def call(p):
    fn, _, args, _ = p
    return Call(fn, args)


@pg.production('ns : decllist')
def ns(p):
    return Ns(p[0])


class SyntaxError(Exception):
    def __init__(self, message, lineno, colno):
        self.message = message
        self.lineno = lineno
        self.colno = colno


@pg.error
def error_handler(token):
    source_pos = token.getsourcepos()
    raise SyntaxError(
        "Got {0} when not expected".format(token.gettokentype()),
        source_pos.lineno,
        source_pos.colno,
    )


parser = pg.build()


def parse(text):
    return parser.parse(lexer.lex(text))
