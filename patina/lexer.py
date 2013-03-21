from ply import lex as plylex


class Lexer(object):
    def build(self, *args, **kwargs):
        self.lexer = plylex.lex(object=self, *args, **kwargs)

    def input(self, text):
        self.lexer.input(text)

    def __iter__(self):
        return iter(self.lexer)

    # keywords = (
    #     'STRUCT',
    #     'FN',
    #     'LET',
    # )

    # List of token names.   This is always required
    tokens = (
        'ID',

        'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',

        #'EQUALS',

        'LPAREN', 'RPAREN',
        #'LBRACKET', 'RBRACKET',
        #'LBRACE', 'RBRACE',

        #'COMMA', 'SEMI', 'COLON',
    )

    # Regular expression rules for simple tokens
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'


    # A regular expression rule with some action code
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t


    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)


    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'


    # Error handling rule
    def t_error(self, t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)


def lex(text):
    l = Lexer()
    l.build()
    l.input(text)
    return l
