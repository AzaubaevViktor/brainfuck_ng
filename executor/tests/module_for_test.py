class Main:
    NAME = "at"
    some_text = "text"

    def __init__(self, *args):
        pass

    def __call__(self):
        return {
            '@': self,
            'some_text': self.some_text,
            'some_method': self._power
        }

    def _power(self, a, b, executor):
        return executor(a) ** executor(b)

    def shutdown(self):
        pass
