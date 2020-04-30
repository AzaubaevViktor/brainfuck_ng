from lexer import ProgramT, Lemma


class Executor:
    def __init__(self, variables: dict):
        self.variables = variables

    def __call__(self, program: ProgramT):
        result = None

        if isinstance(program, Lemma):
            result = self._call_lemma(program)
        else:
            for item in program:
                result = self.call_item(item)

        return result

    def call_item(self, item):
        if isinstance(item, tuple):
            return self._call_tuple(item)
        elif isinstance(item, Lemma):
            return self._call_lemma(item)

        raise TypeError("Unknown type", type(item), item)

    def _call_lemma(self, item):
        return self.variables[item.text]

    def sub(self) -> "Executor":
        # Todo: inserted dicts
        new_variables = self.variables

        return Executor(new_variables)

    def _call_tuple(self, program: tuple):
        func = self.call_item(program[0])
        args = program[1:]

        return func(*args, calc=self.call_item, executor=self)
