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
    pass


# Literals
@pg.production('expr : NUMBER')
def literal(p):
    return Number(p[0].getstr())


@pg.production('expr : LPAREN expr RPAREN')
@pg.production('expr : LBRACKET expr RBRACKET')
@pg.production('expr : LBRACE expr RBRACE')
def group(p):
    return p[1]


# Operators
@pg.production('expr : expr EQUALS expr')
@pg.production('expr : expr PLUS expr')
@pg.production('expr : expr MINUS expr')
def binop(p):
    binop_map = {
        'PLUS': Plus,
        'MINUS': Minus,
        'EQUALS': Equals,
    }
    token_type = p[1].gettokentype()
    return binop_map[token_type](p[0], p[2])


def minus(p):
    return Minus(p[0], p[2])


parser = pg.build()


def parse(text):
    return parser.parse(lexer.lex(text))
