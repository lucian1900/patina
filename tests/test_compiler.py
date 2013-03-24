from patina.ast import *
from patina.compiler import compile


def test_simple():
    fn = Fn(
        Id('main'),
        [],
        Id('int'),
        Block([], None),
    )
    assert compile(fn) == 'int main() {}'


def test_hello():
    fn = Fn(
        Id('main'),
        [],
        Id('int'),
        Block([
            Stmt(Call(Id('print'), [Number(1)])),
        ], None),
    )
    assert compile(fn) == 'int main() {printf("%d", 1); }'
