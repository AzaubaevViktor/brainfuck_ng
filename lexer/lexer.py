from typing import Union

from .sources import BaseSource, StringSource
from .expr import LexerResultT, Expression
from .lemma import Lemma

DIVIDERS = ' \t\n'


def do_lex(source: Union[BaseSource, str]) -> LexerResultT:
    lexer = _Lexer(source)

    return lexer()

class _Lexer:
    def __init__(self, source: Union[BaseSource, str]):
        if isinstance(source, str):
            source = StringSource(source)

        self.source = source

        self.root_obj = Expression(type_first_char='(')

        self.ns_stack = [self.root_obj]

        self.line_num = 0
        self.pos_num = 0

    def __call__(self):
        for symbol in self.source:
            if symbol == '\n':
                self.line_num += 1
                self.pos_num = 0

            self.pos_num += 1

            current = self.ns_stack[-1]

            self._default_mode(current, symbol)

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
        else:
            if isinstance(current, Lemma):
                current.append(symbol)
            else:
                self.ns_stack.append(current.append(Lemma(
                    self.source, symbol, self.line_num, self.pos_num
                )))
