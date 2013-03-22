from rply import ParserGenerator

from patina.lexer import lexer


pg = ParserGenerator(
    [rule.name for rule in lexer.rules],
    precedence=[],
    cache_id='patina',
)


@pg.production("main : expr")
def main(p):
    # p is a list, of each of the pieces on the right hand side of the
    # grammar rule
    return p[0]


parser = pg.build()
