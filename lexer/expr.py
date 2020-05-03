from typing import Union, Sequence, List

from .exc import LexerError
from .lemma import Lemma

ExpressionT = Union[Lemma, "Expression", Sequence['ExpressionT']]
LexerResultT = Union[Lemma, Sequence["LexerResultT"]]


class Expression:
    types = {
        '(': (tuple, ')'),
        '[': (list, ']'),
    }

    def __init__(self, type_first_char: str = None,
                 items: Sequence[ExpressionT] = None):
        self.type = None
        if type_first_char:
            self.set_type(type_first_char)
        self.lemmas: List[ExpressionT] = list(items or [])

    def append(self, item: ExpressionT):
        self.lemmas.append(item)
        return item

    def set_type(self, type_first_char: str):
        if type_first_char not in self.types:
            raise LexerError(type_first_char)
        self.type = type_first_char

    def check_type(self, type_last_char):
        expected_last_char = self.types[self.type][1]
        if expected_last_char != type_last_char:
            raise LexerError(f"Expect {expected_last_char} instead {type_last_char}")

    def compile(self) -> LexerResultT:
        return self._apply_type()

    def _apply_type(self):
        gen = (lemma.compile() if isinstance(lemma, Expression) else lemma
               for lemma in self.lemmas)
        return self.types[self.type][0](gen)

    def sub_ns(self, type_first_char: str) -> "Expression":
        return self.append(Expression(type_first_char=type_first_char))
