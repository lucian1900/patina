from patina.parser import parse


def test_empty():
    assert parse('') is None
