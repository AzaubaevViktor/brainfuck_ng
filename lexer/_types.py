from typing import Union, Sequence

from .lemma import Lemma

ExpressionT = Union[Lemma, "Expression", Sequence['ExpressionT']]
LexerResultT = Union[Lemma, Sequence["LexerResultT"]]