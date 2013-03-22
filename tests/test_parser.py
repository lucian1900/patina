from patina.parser import parse
from patina import ast


def test_simple():
    assert parse('1').value == 1
