import operator
from typing import List, Union

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
            # TODO: Wrong arguments Exception
            assert len(arguments) == len(args)

            sub = executor.sub()

            for arg_lemma, arg in zip(arguments, args):
                # TODO: Error while argument calculation Exception
                sub.variables[arg_lemma.text] = calc(arg)

            return sub(commands)

        new_func.__name__ = f"generated_{name.text}"

        executor.variables[name.text] = new_func

        return defn

    def to_int(lemma: Lemma, calc, executor: Executor):
        return int(lemma.text)

    def add(*lemmas: Lemma, calc, executor: Executor):
        return sum(calc(lemma) for lemma in lemmas)

    def do_set(var_name_: Lemma, value_: Union[tuple, Lemma], calc, executor: Executor):
        value = calc(value_)
        var_name_ = var_name_.text

        executor.variables[var_name_] = value

    variables = {
        'hello': 'world',
        'add': add,
        'append': append_,
        'ret': ret_,
        'x': 'x_value',
        'y': 'y_value',
        'int': to_int,
        'defn': defn,
        'set': do_set,
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
    ("(set new_var (int 1)) new_var", 1),
    ("(set check (int 1))"
     "(append check)"
     "(defn test [a] ("
     "    (set check a)"
     "    (append check)"
     "))"
     "(append check)"
     "(test (int 2)"
     "(ret)", [('check', 1), ('check', 2), ('check', 1)])
    # TODO: Test to inherited variables in Executor
]


@pytest.mark.parametrize('programm, expected', checks)
def test_executor(executor, programm, expected):
    lex_result = do_lex(programm)
    result = executor(lex_result)
    print(result)
    assert expected == result
