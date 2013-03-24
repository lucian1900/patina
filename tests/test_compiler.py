from patina.ast import *


def test_simple():
    fn = Fn(
        Id('main'),
        FieldList([]),
        Id('int'),
        Block([], None),
    )

    assert fn.compile() == 'int main() {}'
