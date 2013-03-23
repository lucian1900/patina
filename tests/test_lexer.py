from ply.lex import *
from patina.lexer import lex


def values(tokens):
    return [t.value for t in tokens]


def test_simple():
    assert values(lex('(1 + 2)')) == ['(', '1', '+', '2', ')']
    assert values(lex('1 == 2')) == ['1', '==', '2']


def test_fn():
    assert values(lex('fn hello() {}')) == [
        'fn', 'hello', '(', ')', '{', '}',
    ]
    assert values(lex('fn hello(a: int) {}')) == [
        'fn', 'hello', '(', 'a', ':', 'int', ')', '{', '}',
    ]
    assert values(lex('fn hello() -> int {}')) == [
        'fn', 'hello', '(', ')', '->', 'int', '{', '}',
    ]
    assert values(lex('fn hello(a: int) -> int { a == 1 }')) == [
        'fn', 'hello', '(', 'a', ':', 'int', ')', '->', 'int',
        '{', 'a', '==', '1', '}',
    ]


def test_struct():
    assert values(lex('struct { a: int }')) == [
        'struct', '{', 'a', ':', 'int', '}'
    ]


def test_let():
    assert values(lex('let a: int = 1')) == ['let', 'a', ':', 'int', '=', '1']
