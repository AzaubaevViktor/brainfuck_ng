from typing import Union

from .sources import BaseSource, StringSource
from .expr import LexerResultT, Expression
from .lemma import Lemma


def do_lex(source: Union[BaseSource, str]) -> LexerResultT:
    if isinstance(source, str):
        source = StringSource(source)

    root_obj = Expression()
    root_obj.set_type('(')

    ns_stack = [root_obj]

    line_num = 0
    pos_num = 0

    for symbol in source:
        if symbol == '\n':
            line_num += 1
            pos_num = 0

        pos_num += 1

        current = ns_stack[-1]

        if symbol in ('(', '['):
            if isinstance(current, Lemma):
                raise NotImplementedError()
            else:
                ns_stack.append(current.sub_ns(symbol))
        elif symbol in (')', ']'):
            if isinstance(current, Lemma):
                ns_stack.pop()
                current = ns_stack[-1]

            current.check_type(symbol)
            ns_stack.pop()
        elif symbol in DIVIDERS:
            if isinstance(current, Lemma):
                ns_stack.pop()
            else:
                pass
        else:
            if isinstance(current, Lemma):
                current.append(symbol)
            else:
                ns_stack.append(current.append(Lemma(
                    source, symbol, line_num, pos_num
                )))

    root_obj.check_type(')')

    return root_obj.compile()


DIVIDERS = ' \t\n'