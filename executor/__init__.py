from lexer import ProgramT


class Executor:
    def __init__(self, ns: dict):
        self.ns = ns

    def __call__(self, program: ProgramT):
        raise NotImplementedError()
