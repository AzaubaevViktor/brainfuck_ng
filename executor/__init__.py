from lexer import ProgramT, NameSpace, Lemma


class Executor:
    def __init__(self, variables: dict):
        self.variables = variables

    def __call__(self, program: ProgramT):
        result = None

        for item in program:
            if isinstance(item, tuple):
                result = self._call(item)
            elif isinstance(item, Lemma):
                result = self.variables[item.text]

        return result

    def _call(self, program: tuple):
        raise NotImplementedError()
