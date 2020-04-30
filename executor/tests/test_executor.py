import operator
from typing import List

import pytest

from executor import Executor
from lexer import Lemma, do_lex, NameSpace


@pytest.fixture(scope='function')
def executor():
    items = []

    def append_(lemma: Lemma, calc, executor):
        items.append((lemma.text, calc(lemma)))

    def ret_(calc, executor):
        return items

    def defn(name: Lemma, arguments: List[Lemma], commands: tuple, calc, executor: Executor):
        def new_func(*args, calc, executor: Executor):
            assert len(arguments) == len(args)

            sub = executor.sub()

            for arg_lemma, arg in zip(arguments, args):
                sub.variables[arg_lemma.text] = calc(arg)

            return sub(commands)

        new_func.__name__ = f"generated_{name.text}"

        executor.variables[name.text] = new_func

        return defn

    def to_int(lemma: Lemma, calc, executor: Executor):
        return int(lemma.text)

    def add(*lemmas: Lemma, calc, executor: Executor):
        return sum(calc(lemma) for lemma in lemmas)

    variables = {
        'hello': 'world',
        'add': add,
        'append': append_,
        'ret': ret_,
        'x': 'x_value',
        'y': 'y_value',
        'int': to_int,
        'defn': defn
    }

    return Executor(variables)


checks = [
    ("hello", "world"),
    ("(append x) (append  y) (ret)", [('x', 'x_value'), ('y', 'y_value')]),
    ("(int 10)", 10),
    ("(int -10)", -10),
    ("(int 1234)", 1234),
    ("(add (int 1) (int 2))", 3),
    ("(defn test [a b] ( (add a b) )) (test (int 1) (int 2))", 3),
    ("(defn test [a b] ( (add (int 1) a b) (add a b) )) (test (int 1) (int 2))", 3),
    # TODO: Test to inherited variables in Executor
]


@pytest.mark.parametrize('programm, expected', checks)
def test_executor(executor, programm, expected):
    lex_result = do_lex(programm)
    result = executor(lex_result)
    assert expected == result
