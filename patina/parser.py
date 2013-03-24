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
def main(p):
    return p[0]


@pg.production('id : ID')
def identifier(p):
    return Id(p[0].getstr())


@pg.production('field : id COLON id')
def field_typed(p):
    name, _, type = p
    return Field(name, type)


@pg.production('field : id')
def field_inferred(p):
    return Field(p[0], None)


@pg.production('fieldlist : field')
@pg.production('fieldlist : fieldlist COMMA field')
def fieldlist(p):
    if len(p) == 1:
        return FieldList(p)
    else:
        flist, _, field = p
        return FieldList(flist.fields + [field])


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
    return Statement(expr)


@pg.production('block : LBRACE expr RBRACE')
def block(p):
    _, exprs, _ = p
    return Block(exprs)


@pg.production('expr : block')
def block_expr(p):
    return p[0]


@pg.production('let : LET field ASSIGN expr')
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


@pg.production('fn : FN id LPAREN fieldlist RPAREN RETURNS id block')
def fn(p):
    _, name, _, fields, _, _, returns, block = p
    return Fn(name, fields, returns, block)


@pg.production('decl : fn')
def fn_stmt(p):
    return p[0]


# Literals
@pg.production('expr : NUMBER')
def literal(p):
    return Number(p[0].getstr())


@pg.production('exprlist : expr')
@pg.production('exprlist : exprlist COMMA expr')
def exprlist(p):
    if len(p) == 1:
        return p
    else:
        elist, _, expr
        return elist + [expr]


# Array
@pg.production('expr : LBRACKET exprlist RBRACKET')
def array(p):
    return Array(p[1])


# Call
@pg.production('expr : id LPAREN exprlist RPAREN')
def call(p):
    fn, _, args, _ = p
    return Call(fn, args)


# Operators
@pg.production('expr : expr EQUALS expr')
@pg.production('expr : expr PLUS expr')
@pg.production('expr : expr MINUS expr')
def binop(p):
    left, op, right = p
    binop_map = {
        'PLUS': Plus,
        'MINUS': Minus,
        'EQUALS': Equals,
    }
    op_type = op.gettokentype()
    return binop_map[op_type](left, right)


@pg.error
def error_handler(token):
    source_pos = token.getsourcepos()
    raise ValueError(
        "Line {line}, col {col}: Got {type} when not expected".format(
            line=source_pos.lineno,
            col=source_pos.colno,
            type=token.gettokentype(),
        )
    )


parser = pg.build()


def parse(text):
    return parser.parse(lexer.lex(text))
