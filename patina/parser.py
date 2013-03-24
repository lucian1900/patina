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


@pg.production('type : COLON id')
def type_(p):
    _, id = p
    return id


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


@pg.production('fieldlist :')
@pg.production('fieldlist : field')
@pg.production('fieldlist : fieldlist COMMA field')
def fieldlist(p):
    if len(p) == 0:
        return FieldList([])
    elif len(p) == 1:
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
    return Stmt(expr)


@pg.production('stmtlist : stmt')
@pg.production('stmtlist : stmtlist stmt')
def stmt_list(p):
    if len(p) == 1:
        return p
    else:
        slist, stmt = p
        return slist + [stmt]


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


@pg.production('fn : FN id LPAREN fieldlist RPAREN RETURNS id block')
def fn_returns(p):
    _, name, _, fields, _, _, returns, block = p
    return Fn(name, fields, returns, block)


@pg.production('fn : FN id LPAREN fieldlist RPAREN block')
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


@pg.production('exprlist : expr')
@pg.production('exprlist : exprlist COMMA expr')
def expr_list(p):
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
