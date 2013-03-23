from rply import ParserGenerator

from patina.lexer import lexer
from patina.ast import *


pg = ParserGenerator(
    [rule.name for rule in lexer.rules],
    precedence=[],
    cache_id='patina',
)


@pg.production('main : expr')
def main(p):
    # p is a list, of each of the pieces on the right hand side of the
    # grammar rule
    return p[0]


@pg.production('expr : ID')
def identifier(p):
    return Id(p[0].getstr())


# Literals
@pg.production('expr : NUMBER')
def literal(p):
    return Number(p[0].getstr())


@pg.production('expr : LPAREN expr RPAREN')
@pg.production('expr : LBRACKET expr RBRACKET')
def group(p):
    left, expr, right = p
    return expr


@pg.production('expr : LBRACE expr RBRACE')
def block(p):
    _, exprs, _ = p
    return Block(exprs)


@pg.production('expr : LET ID COLON ID ASSIGN expr')
def let(p):
    _, name, _, type, _, _, expr = p
    return Let(name, type, expr)


@pg.production('expr : IF expr LBRACE expr RBRACE ELSE LBRACE expr RBRACE')
def if_(p):
    _, condition, _, then, _, _, _, otherwise, _ = p
    return If(condition, then, otherwise)


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
