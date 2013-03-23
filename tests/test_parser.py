from patina.parser import parse
from patina.ast import *


def test_simple():
    assert parse('1') == Number(1)
    assert parse('1 + 2') == Plus(Number(1), Number(2))
    assert parse('hello') == Id('hello')
    assert parse('1 + x') == Plus(Number(1), Id('x'))


def test_fields():
    assert parse('a: int') == FieldList([Field(Id('a'), Id('int'))])
    assert parse('a: int, b: str') == FieldList([
        Field(Id('a'), Id('int')),
        Field(Id('b'), Id('str')),
    ])


def test_block():
    #assert parse('{}') == Block(None)
    assert parse('{ 1 }') == Block(Number(1))


def test_let():
    assert parse('let a: int = 1') == Let(Id('a'), Id('int'), Number('1'))


def test_fn():
    assert parse('fn add(a: int, b: int) -> int { a }') == Fn(
        Id('add'),
        FieldList(
            Field(Id('a'), Id('int')),
            Field(Id('b'), Id('int')),
        ),
        Id('int'),
        Block(Id('a')),
    )


def test_if():
    assert parse('if 1 { 2 } else { 3 }') == If(
        Number(1), Block(Number(2)), Block(Number(3)))
