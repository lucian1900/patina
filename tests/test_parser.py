from patina.parser import parse
from patina.ast import *


def test_simple():
    assert parse('1') == Number(1)
    assert parse('hello') == Id('hello')
    assert parse('1;') == Stmt(Number(1))


def test_block():
    assert parse('{}') == Block([], None)
    assert parse('{ 1 }') == Block([], Number(1))
    assert parse('{ 1; 2 }') == Block([Stmt(Number(1))], Number(2))
    assert parse('{ 1; 2; }') == Block(
        [Stmt(Number(1)), Stmt(Number(2))],
        None,
    )


def test_let():
    assert parse('let a = 1') == Let(Field(Id('a'), None), Number(1))
    assert parse('let a: int = 1') == Let(
        Field(Id('a'), Type('int')),
        Number('1'),
    )


def test_fn():
    assert parse('fn foo() {}') == Fn(
        Id('foo'), [], None, Block([], None),
    )

    assert parse('fn foo(a: int) {}') == Fn(
        Id('foo'),
        [Field(Id('a'), Type('int'))],
        None,
        Block([], None),
    )

    assert parse('fn add(a: int, b: int) -> int { a }') == Fn(
        Id('add'),
        [
            Field(Id('a'), Type('int')),
            Field(Id('b'), Type('int')),
        ],
        Id('int'),
        Block([], Id('a')),
    )


def test_call():
    assert parse('print()') == Call(Id('print'), [])
    assert parse('print(1)') == Call(Id('print'), [Number(1)])
    assert parse('add(1, 2)') == Call(Id('add'), [Number(1), Number(2)])
    assert parse('add(1, x)') == Call(Id('add'), [Number(1), Id('x')])


def test_array():
    assert parse('[]') == Array([])
    assert parse('[1]') == Array([Number(1)])
    assert parse('[1, 2]') == Array([Number(1), Number(2)])


def test_if():
    assert parse('if 1 { 2 }') == If(Number(1), Block([], Number(2)), None)
    assert parse('if 1 { 2 } else { 3 }') == If(
        Number(1),
        Block([], Number(2)),
        Block([], Number(3)),
    )


def test_struct():
    assert parse('struct a {x: int}') == Struct(
        Id('a'),
        [Field(Id('x'), Type('int'))],
    )


def test_hello():
    assert parse('fn main() { print(1); }') == Fn(
        Id('main'),
        [],
        None,
        Block([Stmt(
            Call(Id('print'), [Number(1)]),
        )], None),
    )


def test_ns():
    assert parse('''
    struct foo {a : int}
    fn main() {}
    ''') == Ns([
        Struct(Id('foo'), [Field(Id('a'), Type('int'))]),
        Fn(Id('main'), [], None, Block([], None)),
    ])
