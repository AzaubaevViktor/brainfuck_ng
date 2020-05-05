from typing import Union, List

from . import LexerError
from .sources import BaseSource, StringSource
from .expr import LexerResultT, Expression, ExpressionT
from .lemma import Lemma, StringLemma

DIVIDERS = ' \t\n'
STRING_START = '\"'
STRING_END = '\"'


def do_lex(source: Union[BaseSource, str]) -> LexerResultT:
    return BaseLexer(source)()


class BaseLexer:
    def __init__(self, source: Union[BaseSource, str]):
        if isinstance(source, str):
            source = StringSource(source)

        self.source = source

        self.root_obj = Expression(type_first_char='(')

        self.ns_stack: List[ExpressionT] = [self.root_obj]

        self.line_num = 1
        self.pos_num = 0

    def __call__(self) -> LexerResultT:
        for symbol in self.source:
            if symbol == '\n':
                self.line_num += 1
                self.pos_num = 0

            self.pos_num += 1

            current = self.ns_stack[-1]

            if isinstance(current, StringLemma) and not current.finished:
                self._string_mode(current, symbol)
            else:
                self._default_mode(current, symbol)

        while self.ns_stack and isinstance(self.ns_stack[-1], Lemma):
            self.ns_stack.pop()

        if len(self.ns_stack) != 1:
            raise LexerError(self.ns_stack)

        self.root_obj.check_type(')')

        return self.root_obj.compile()

    def _default_mode(self, current, symbol):
        if symbol in ('(', '['):
            if isinstance(current, Lemma):
                raise NotImplementedError()
            else:
                self.ns_stack.append(current.sub_ns(symbol))
        elif symbol in (')', ']'):
            if isinstance(current, Lemma):
                self.ns_stack.pop()
                current = self.ns_stack[-1]

            current.check_type(symbol)
            self.ns_stack.pop()
        elif symbol in DIVIDERS:
            if isinstance(current, Lemma):
                self.ns_stack.pop()
            else:
                pass
        elif symbol in STRING_START:
            self.ns_stack.append(current.append(StringLemma(
                self.source, "", self.line_num, self.pos_num
            )))
        else:
            if isinstance(current, Lemma):
                current.append(symbol)
            else:
                self.ns_stack.append(current.append(Lemma(
                    self.source, symbol, self.line_num, self.pos_num
                )))

    def _string_mode(self, current: StringLemma, symbol: str):
        if current.escaping:
            current.process_escape(symbol)
            return

        if symbol == '\\':
            current.escaping = True
            return

        if symbol in STRING_END:  # TODO: and not escape
            current.finished = True
            self.ns_stack.pop()
            return

        current.text += symbol
