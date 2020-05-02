from typing import List, Union

import pytest

from executor import Executor
from executor.tests.module_for_test import Main
from lexer import Lemma, LexerResultT


@pytest.fixture(scope='function')
def executor():
    items = []

    def append_(lemma: Lemma, calc, executor):
        items.append((lemma.text if isinstance(lemma, Lemma) else type(lemma), calc(lemma)))

    def ret_(calc, executor):
        return items

    def defn(name: Lemma, arguments: List[Lemma], commands: tuple, calc, executor: Executor):
        func_name = f"generated_{name.text}"

        def new_func(*args, calc, executor: Executor):
            # TODO: Wrong arguments Exception
            if len(arguments) != len(args):
                raise TypeError(f"For {func_name}:\nExpect {len(arguments)} argument, but {len(args)}:\n{args}")

            sub = executor.sub()

            for arg_lemma, arg in zip(arguments, args):
                # TODO: Error while argument calculation Exception
                sub.variables[arg_lemma.text] = calc(arg)

            return sub(commands)

        new_func.__name__ = func_name

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

    modules = {
        Main.NAME: Main
    }

    def _import(module_name: Lemma, calc, executor):
        ModuleClass = modules[module_name.text]
        module = ModuleClass(executor)
        executor.variables.update(module())
        return module

    def get_operator(op_name: Lemma, calc, executor):
        import operator
        op_func = getattr(operator, op_name.text)

        def wrapper_op(*raw_args: LexerResultT, calc, executor):
            args = map(calc, raw_args)
            return op_func(*args)

        wrapper_op.__name__ = f"wrapper_{op_func.__name__}"
        return wrapper_op

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
        'import': _import,
        'op': get_operator,
    }

    return Executor(variables)
