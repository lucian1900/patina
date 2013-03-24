from patina.lexer import lex


def tokens(text):
    return [t.value for t in lex(text)]


def test_simple():
    assert tokens('1') == ['1']
    assert tokens('add(1, 2)') == ['add', '(', '1', ',', '2', ')']


def test_empty():
    assert tokens('') == []
    assert tokens('\n \n') == []


def test_fn():
    assert tokens('fn hello() {}') == [
        'fn', 'hello', '(', ')', '{', '}',
    ]
    assert tokens('fn hello(a: int) {}') == [
        'fn', 'hello', '(', 'a', ':', 'int', ')', '{', '}',
    ]
    assert tokens('fn hello() -> int {}') == [
        'fn', 'hello', '(', ')', '->', 'int', '{', '}',
    ]
    assert tokens('fn hello(a: int) -> int { add(a, 1) }') == [
        'fn', 'hello', '(', 'a', ':', 'int', ')', '->', 'int',
        '{', 'add', '(', 'a', ',', '1', ')', '}',
    ]


def test_struct():
    assert tokens('struct { a: int }') == [
        'struct', '{', 'a', ':', 'int', '}'
    ]


def test_let():
    assert tokens('let a: int = 1') == ['let', 'a', ':', 'int', '=', '1']
