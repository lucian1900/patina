from rply import LexerGenerator

lg = LexerGenerator()
# Identifiers
lg.add('ID',       r'[a-zA-Z_][a-zA-Z_0-9]*')

# Types
lg.add('RETURNS',  r'->')
lg.add('COLON',    r':')

# Operators
lg.add('PLUS',     r'\+')
lg.add('MINUS',    r'-')
lg.add('NUMBER',   r'\d+')
lg.add('EQUALS',   r'==')

# Grouping
lg.add('LPAREN',   r'\(')
lg.add('RPAREN',   r'\)')
lg.add('LBRACKET', r'\[')
lg.add('RBRACKET', r'\]')
lg.add('LBRACE',   r'\{')
lg.add('RBRACE',   r'\}')


# Keywords
lg.add('STRUCT',   r'struct')
lg.add('FN',       r'fn')
lg.add('LET',      r'let')
lg.add('IF',       r'if')


lg.ignore(r' ')
lg.ignore(r'\t')
lg.ignore(r'\#.*')

lexer = lg.build()
#lex = lexer.lex


def lex(text):
    stream = lexer.lex(text)

    tok = stream.next()
    while tok is not None:
        yield tok
        tok = stream.next()
