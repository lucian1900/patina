from rply import LexerGenerator

lg = LexerGenerator()

# Keywords
lg.add('STRUCT',   r'struct')
lg.add('FN',       r'fn')
lg.add('LET',      r'let')
lg.add('ASSIGN',   r'=')
lg.add('IF',       r'if')
lg.add('ELSE',     r'else')

# Types
lg.add('RETURNS',  r'->')
lg.add('COLON',    r':')

lg.add('SEMI',     r';')
lg.add('COMMA',    r',')

# Grouping
lg.add('LPAREN',   r'\(')
lg.add('RPAREN',   r'\)')
lg.add('LBRACKET', r'\[')
lg.add('RBRACKET', r'\]')
lg.add('LBRACE',   r'\{')
lg.add('RBRACE',   r'\}')

# Identifiers
lg.add('ID',       r'[a-zA-Z_][a-zA-Z_0-9]*')

# Literals
lg.add('NUMBER',   r'\d+')
#lg.add('QUOTE',    r'\"')

lg.ignore(r' ')
lg.ignore(r'\n')
lg.ignore(r'\t')
lg.ignore(r'\#.*')

lexer = lg.build()


def lex(text):
    stream = lexer.lex(text)

    tok = stream.next()
    while tok is not None:
        yield tok
        tok = stream.next()
