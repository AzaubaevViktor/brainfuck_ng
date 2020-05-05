from typing import Union, Type, Optional

from lexer import Lemma, LexerResultT, StringLemma, BaseSource
from lexer.lexer import BaseLexer

from .exc import ExecutorError, ErrorStackFrame, PythonExecutorError

"""
TODO: 
Exception:
  * Environment
    * Call stack
    * Variables stack
  * Message
  * Additional info

TODO:
Call stack
Stack item:
  * Source
  * Line
  * Position
  * Stage

"""


VariablesT = Union[dict, "Variables"]


class BaseScope:
    def __init__(self, data: dict):
        self.data = data

    def __getattr__(self, item):
        return self.data[item]


class Variables:
    def __init__(self, parent: VariablesT):
        self.parent = parent
        self.data: Optional[dict] = None

    def __getitem__(self, item: str):
        if self.data and item in self.data:
            return self.data[item]

        if item not in self.parent:
            raise ExecutorError(f'Term `{item}` not found in this scope. Try:\n'
                                ", ".join(self.keys()))

        return self.parent[item]

    def keys(self):
        if self.data:
            yield from self.data.keys()
        yield from self.parent.keys()

    def __setitem__(self, key, value):
        if self.data is None:
            self.data = {}

        self.data[key] = value
        return value

    def get_scope(self, name: str) -> BaseScope:
        return type(
            name,
            (BaseScope, ),
            self.data
        )

    def __contains__(self, item):
        if self.data and item in self.data:
            return True

        if item in self.parent:
            return True

        return False

    def get(self, item, default=None):
        if item in self:
            return self[item]
        return default

    def update(self, new_data, **kwargs):
        if self.data is None:
            self.data = {}
        self.data.update(new_data)
        self.data.update(kwargs)


class Executor:
    def __init__(self, variables: VariablesT, **kwargs):
        self.variables = Variables(variables)
        self.variables.update(kwargs)

    def __call__(self, *program: LexerResultT):
        result = None

        for item in program:
            try:
                if isinstance(item, tuple):
                    result = self._call_tuple(item)
                elif isinstance(item, Lemma):
                    result = self._call_lemma(item)
                elif isinstance(item, list):
                    result = [self(list_item) for list_item in item]
                else:
                    raise TypeError("Unknown type", type(item), item)
            except ExecutorError as e:
                e.append(item)
                raise
            except Exception as orig_e:
                e = PythonExecutorError(orig_e)
                e.append(item)
                raise e

        return result

    def _call_lemma(self, lemma: Lemma):
        if isinstance(lemma, StringLemma):
            return lemma.text

        if (value := self._check_int(lemma)) is not None:
            return value

        return self.variables[lemma.text]

    def _check_int(self, lemma: Lemma):
        try:
            return int(lemma.text)
        except ValueError:
            return None

    def _call_tuple(self, program: tuple):
        if not program:
            raise ExecutorError("Need more than one item in tuple")

        func = self(program[0])
        if not callable(func):
            e = ExecutorError(f"Expect callable instead: `{func}`")
            e.append(program[0])
            raise e
        args = program[1:]

        # TODO: Exception wrapper for function

        return func(*args, executor=self)

    def sub(self) -> "Executor":
        return Executor(self.variables)

    def run(self, source: Union[BaseSource, str], LexerClass: Type[BaseLexer] = BaseLexer):
        lex_results = LexerClass(source)()

        return self(*lex_results)
