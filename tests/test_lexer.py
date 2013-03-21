from ply.lex import *
from patina.lexer import lex


def token_values(tokens):
    return [t.value for t in tokens]


def test_arithmetic():
    assert token_values(lex('(1 + 2)')) == ['(', 1, '+', 2, ')']
