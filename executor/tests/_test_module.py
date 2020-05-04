from executor.builtin._base import BaseModule
from lexer import Lemma


class TestModule(BaseModule):
    NAME = "_test"
    dependencies = ("builtin", )

    def __init__(self):
        from modules.builtin import BaseBuiltin

    def __call__(self, variables):
        return {
            'hello': "world",
            **self._gen_append_ret(),
            'x': 'x_value',
            'y': 'y_value',
            'int': self.to_int,
        }

    def _gen_append_ret(self):
        items = []

        def append_(lemma: 'Lemma', executor):
            items.append((lemma.text if isinstance(lemma, Lemma) else type(lemma), executor(lemma)))

        def ret_(executor):
            return items

        return {
            'append': append_,
            'ret': ret_,
        }

    @staticmethod
    def to_int(lemma: Lemma, executor):
        return int(lemma.text)
