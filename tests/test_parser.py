from patina.parser import parse
from patina import ast


def test_simple():
    assert parse('1').value == 1
    assert parse('1') == ast.Number('1')

    assert parse('1 + 2') == ast.Plus(ast.Number('1'), ast.Number('2'))
