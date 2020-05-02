from typing import Union

from lexer import Lemma, ExpressionT, LexerResultT, StringLemma

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


class Variables:
    def __init__(self, parent: VariablesT):
        self.parent = parent
        self.data = None

    def __getitem__(self, item):
        if self.data and item in self.data:
            return self.data[item]
        return self.parent[item]

    def __setitem__(self, key, value):
        if self.data is None:
            self.data = {}

        self.data[key] = value
        return value

    def update(self, new_data, **kwargs):
        if self.data is None:
            self.data = {}
        self.data.update(new_data)
        self.data.update(kwargs)


class Executor:
    def __init__(self, variables: VariablesT):
        self.variables = Variables(variables)

    def __call__(self, *program: LexerResultT):
        result = None

        for item in program:
            if isinstance(item, tuple):
                result = self._call_tuple(item)
            elif isinstance(item, Lemma):
                result = self._call_lemma(item)
            else:
                raise TypeError("Unknown type", type(item), item)

        return result

    def _call_lemma(self, lemma: Lemma):
        # TODO: Unknown variable Exception
        if isinstance(lemma, StringLemma):
            return lemma.text

        if (value := self._check_int(lemma)):
            return value

        return self.variables[lemma.text]

    def _check_int(self, lemma: Lemma):
        try:
            return int(lemma.text)
        except ValueError:
            return None

    def _call_tuple(self, program: tuple):
        func = self(program[0])
        args = program[1:]

        # TODO: Exception wrapper for function
        return func(*args, executor=self)

    def sub(self) -> "Executor":
        return Executor(self.variables)
