from typing import Union

from lexer import ProgramT, Lemma

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

    def __call__(self, program: ProgramT):
        result = None

        if isinstance(program, Lemma):
            result = self._call_lemma(program)
        else:
            for item in program:
                result = self.calc(item)

        return result

    def calc(self, item):
        if isinstance(item, tuple):
            return self._call_tuple(item)
        elif isinstance(item, Lemma):
            return self._call_lemma(item)

        raise TypeError("Unknown type", type(item), item)

    def _call_lemma(self, item):
        # TODO: Unknown variable Exception
        return self.variables[item.text]

    def sub(self) -> "Executor":
        return Executor(self.variables)

    def _call_tuple(self, program: tuple):
        func = self.calc(program[0])
        args = program[1:]

        # TODO: Exception wrapper for function
        return func(*args, calc=self.calc, executor=self)
