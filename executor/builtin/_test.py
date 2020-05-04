from typing import List, Union

from executor import ExecutorError
from executor.builtin._import import BaseModule
from lexer import Lemma


class TestModule(BaseModule):
    NAME = "_test"

    def __init__(self):
        from .module_for_test import At

    def __call__(self, variables):
        return {**{
            'hello': "world",
            'add': self.add,
            **self._gen_append_ret(),
            'x': 'x_value',
            'y': 'y_value',
            'defn': self.defn,
            'set': self.do_set,
            'op': self.get_operator,
            'int': self.to_int,
        }, **{
            '=': self.do_set,
            '+': self.add,
            'print': self.print
        }}

    @staticmethod
    def add(*lemmas: 'Lemma', executor: 'Executor'):
        return sum(executor(lemma) for lemma in lemmas)

    @staticmethod
    def print(*objs: 'LexerResultT', executor):
        print(*map(executor, objs))

    def _gen_append_ret(self):
        items = []

        def append_(lemma: 'Lemma', executor):
            items.append((lemma.text if isinstance(lemma, Lemma) else type(lemma), executor(lemma)))

        def ret_(executor):
            return items

        return {
            'append': append_,
            'ret': ret_,
        }

    @staticmethod
    def defn(name: Lemma, arguments: List[Lemma], commands: tuple, executor):
        func_name = f"generated_{name.text}"

        argument_names = [arg.text for arg in arguments]

        def new_func(*args, executor):
            # TODO: Wrong arguments Exception

            if len(argument_names) > len(args):
                expected_argument = argument_names[len(args)]
                raise ExecutorError(f"{func_name}: Expect argument {expected_argument}")

            if len(argument_names) < len(args):
                raise ExecutorError(f"{func_name}: Too many arguments (expect {len(argument_names)})")

            sub = executor.sub()

            for arg_name, arg in zip(argument_names, args):
                # TODO: Error while argument calculation Exception
                sub.variables[arg_name] = executor(arg)

            return sub(*commands)

        new_func.__name__ = func_name

        executor.variables[name.text] = new_func

        return new_func

    @staticmethod
    def do_set(var_name_: Lemma, value_: Union[tuple, Lemma], executor):
        value = executor(value_)
        var_name_ = var_name_.text

        executor.variables[var_name_] = value

        return value

    @staticmethod
    def get_operator(op_name: Lemma, executor):
        import operator
        op_func = getattr(operator, op_name.text)

        def wrapper_op(*raw_args: "LexerResultT", executor):
            args = map(executor, raw_args)
            return op_func(*args)

        wrapper_op.__name__ = f"wrapper_{op_func.__name__}"
        return wrapper_op

    @staticmethod
    def to_int(lemma: Lemma, executor):
        return int(lemma.text)
