import operator

import pytest

from executor import Executor
from lexer import Lemma, do_lex


@pytest.fixture(scope='function')
def executor():
    items = []

    def append_(lemma: Lemma, executor):
        items.append((lemma.text, executor(lemma)))

    def ret_(executor):
        return items

    variables = {
        'hello': 'world',
        'add': operator.add,
        'append': append_,
        'ret': ret_,
        'x': 'x_value',
        'y': 'y_value',
    }

    return Executor(variables)


checks = [
    ("hello", "world"),
    ("add", operator.add),
    ("(append x) (append  y) (ret)", [('x', 'x_value'), ('y', 'y_value')])
]


@pytest.mark.parametrize('programm, expected', checks)
def test_executor(executor, programm, expected):
    lex_result = do_lex(programm)
    result = executor(lex_result)
    assert expected == result
