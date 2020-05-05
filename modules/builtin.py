from typing import List, Union

from executor import ExecutorError
from executor.builtin._base import BaseModule
from lexer import Lemma, LexerResultT


class BaseBuiltin(BaseModule):
    NAME = "builtin"

    def __call__(self, variables):
        return {
            '=': self.do_set,
            '+': self.add,
            '*': self.mul,
            '/': self.div,
            'print': self.print,
            'defn': self.defn,
            'op': self.get_operator,
            '.': self._getattr,
            '.=': self._setattr,
            'item': self._getitem,
            'item=': self._setitem,
            'True': True,
            'False': False,
            'exit': self._exit
        }

    @staticmethod
    def _getattr(obj: LexerResultT, attr: Lemma, executor):
        return getattr(executor(obj), attr.text)

    @staticmethod
    def _setattr(obj_: LexerResultT, attr_: Lemma, value_: LexerResultT, executor):
        attr = attr_.text
        obj = executor(obj_)
        value = executor(value_)

        setattr(obj, attr, value)

        return value

    @staticmethod
    def _getitem(obj: LexerResultT, item: LexerResultT, executor):
        return executor(obj).__getitem__(executor(item))

    @staticmethod
    def _setitem(obj: LexerResultT, item: LexerResultT, value: LexerResultT, executor):
        _value = executor(value)
        executor(obj).__setitem__(executor(item), _value)
        return _value

    @staticmethod
    def add(*lemmas: LexerResultT, executor: 'Executor'):
        return sum(executor(lemma) for lemma in lemmas)

    @staticmethod
    def mul(*lemmas: LexerResultT, executor: 'Executor'):
        result = 1
        for lemma in lemmas:
            result *= executor(lemma)

        return result

    @staticmethod
    def div(a: LexerResultT, b: LexerResultT, executor):
        return executor(a) / executor(b)

    @staticmethod
    def print(*objs: 'LexerResultT', executor):
        print(*map(executor, objs))

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
    def _exit(code: LexerResultT, executor):
        exit(executor(code))
