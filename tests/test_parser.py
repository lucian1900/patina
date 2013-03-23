from patina.parser import parse
from patina.ast import *


def test_simple():
    assert parse('1') == Number(1)
    assert parse('1 + 2') == Plus(Number(1), Number(2))
    assert parse('hello') == Id('hello')
    assert parse('{ 1 }') == Block(Number(1))


def test_let():
    assert parse('let a: int = 1') == Let(Id('a'), Id('int'), Number('1'))


def test_if():
    assert parse('if 1 { 2 } else { 3 }') == If(
        Number(1), Number(2), Number(3))
