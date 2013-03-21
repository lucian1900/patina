from ply.lex import *
from patina.lexer import lex


def values(tokens):
    return [t.value for t in tokens]


def test_arithmetic():
    assert values(lex('(1 + 2)')) == ['(', 1, '+', 2, ')']


def test_fn():
    assert values(lex('fn hello(a: int) -> { a == 1 }')) == [
        'fn', 'hello', '(', 'a', ':', 'int', ')', '->', '{', 'a', '==', 1, '}'
    ]


def test_struct():
    assert values(lex('struct { a: int }')) == [
        'struct', '{', 'a', ':', 'int', '}'
    ]
