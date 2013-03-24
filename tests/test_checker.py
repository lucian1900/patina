from patina.ast import *
from patina.parser import parse


def test_simple():
    let = parse('let a = 1')

    assert let.type == Type('int')
