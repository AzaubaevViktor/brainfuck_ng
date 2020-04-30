class Executor:
    def __init__(self, ns: dict):
        self.ns = ns

    def __call__(self, programm):
        raise NotImplementedError()
