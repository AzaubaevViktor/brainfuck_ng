from lexer import Program


class Executor:
    def __init__(self, ns: dict):
        self.ns = ns

    def __call__(self, program: Program):
        raise NotImplementedError()
