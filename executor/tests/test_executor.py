import operator

import pytest

from executor import Executor
from lexer import Lemma


@pytest.fixture(scope='function')
def executor():
    items = []

    def append_(lemma: Lemma):
        items.append(lemma.text)

    def ret_():
        return items

    ns = {
        'hello': 'world',
        'add': operator.add,
        'append': append_,
        'ret': ret_,
    }

    return Executor(ns)


checks = [
    ("hello", "world"),
    ("add", operator.add),
    ("(append x) (append  y) (ret)", ['x', 'y'])
]


@pytest.mark.parametrize('programm, expected', checks)
def test_executor(executor, programm, expected):
    result = executor(programm)
    assert expected == result
