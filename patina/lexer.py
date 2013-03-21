import ply.lex
from ply.lex import TOKEN

digit            = r'([0-9])'
nondigit         = r'([_A-Za-z])'
identifier       = r'(' + nondigit + r'(' + digit + r'|' + nondigit + r')*)'

keywords = {
    'struct': 'STRUCT',
    'fn': 'FN',
    'let': 'LET',
    'if': 'IF',
}

# List of token names.   This is always required
tokens = [
    'ID',

    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',

    'ASSIGN', 'EQUALS', 'RETURNS',

    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE',

    'COMMA', 'SEMI', 'COLON',


] + list(keywords.values())

# Regular expression rules for simple tokens
t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_RETURNS  = r'->'
t_EQUALS   = r'=='
t_COLON    = r':'


@TOKEN(identifier)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = keywords.get(t.value, 'ID')
    return t


# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
t_ignore_COMMENT = r'\#.*'


# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


def lex(text):
    l = ply.lex.lex()
    l.input(text)
    return l
