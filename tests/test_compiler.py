from patina.ast import *
from patina.compiler import CompilerContext


def test_simple():
    fn = Fn(
        Id('main'),
        FieldList([]),
        Id('int'),
        Block([], None),
    )
    assert fn.compile(CompilerContext()) == 'int main() {}'


def test_hello():
    fn = Fn(
        Id('main'),
        FieldList([]),
        Id('int'),
        Block([
            Stmt(Call(Id('print'), [Number(1)])),
        ], None),
    )
    assert fn.compile(CompilerContext()) == 'int main() {printf("%d", 1); }'
