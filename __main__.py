"""
TODO:

Install wrapper for packages
Run file
Add extensions (modules) dir
Interactive mode

"""
import sys
from traceback import print_exc
from typing import Union

from executor import Executor
from lexer import LexerResultT, Lemma, do_lex


def do_set(var_name_: Lemma, value_: Union[tuple, Lemma], executor: Executor):
    value = executor(value_)
    var_name_ = var_name_.text

    executor.variables[var_name_] = value

    return value


def _getattr(obj: LexerResultT, attr: Lemma, executor: Executor):
    return getattr(executor(obj), attr.text)


def _setattr(obj_: LexerResultT, attr_: Lemma, value_: LexerResultT, executor: Executor):
    attr = attr_.text
    obj = executor(obj_)
    value = executor(value_)

    setattr(obj, attr, value)

    return value


def _getitem(obj: LexerResultT, item: LexerResultT, executor):
    return executor(obj).__getitem__(executor(item))


def _setitem(obj: LexerResultT, item: LexerResultT, value: LexerResultT, executor):
    _value = executor(value)
    executor(obj).__setitem__(executor(item), _value)
    return _value


def get_operator(op_name: Lemma, executor):
    import operator
    op_func = getattr(operator, op_name.text)

    def wrapper_op(*raw_args: LexerResultT, executor):
        args = map(executor, raw_args)
        return op_func(*args)

    wrapper_op.__name__ = f"wrapper_{op_func.__name__}"
    return wrapper_op


def _print(*objs: LexerResultT, executor):
    print(*map(executor, objs))


def _do_exit(executor):
    exit()


variables = {
    'about': "REPL v0",
    'version': 0,
    '@': globals(),
    '.': _getattr,
    '.=': _setattr,
    'item': _getitem,
    'item=': _setitem,
    'op': get_operator,
    'exit': _do_exit,
    '=': do_set,
    "print": _print,
}


executor = Executor(variables)

_init = """
(print "Hello from LolLisp interpreter!")
(print "Version:" version)
(print "Little magic here...")

(= @exec (item @ "executor"))
(= @vars (. (item @ "executor") variables))

(print "Now you can use `@exec` and `@vars`")
(print "Enjoy!")
"""

executor(*do_lex(_init))

if __name__ == '__main__':
    while True:
        sys.stdout.flush()
        sys.stderr.flush()

        s = input("~~> ")
        try:
            lex_result = do_lex(s)
            print(lex_result)
            print(executor(*lex_result))
        except:
            print_exc()
        finally:
            print()

