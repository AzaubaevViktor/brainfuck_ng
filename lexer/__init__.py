from typing import Iterable, Union, List, Sequence, Tuple


class LexerError(Exception):
    pass


class BaseSource:
    def __iter__(self) -> Iterable[str]:
        raise NotImplementedError()


class StringSource:
    def __init__(self, data: str):
        self.data = data

    def __iter__(self):
        yield from self.data

    def __repr__(self):
        return f"<StrSource({len(self.data)})>"


class Lemma:
    def __init__(self, source: BaseSource, text: str, line: int, pos: int):
        self.source = source
        self.text = text
        self.line = line
        self.pos = pos

    def append(self, ch):
        self.text += ch

    def __repr__(self):
        return f"<Lemma:{self.source}:{self.line}:{self.pos} `{self.text}`>"


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
        assert self.types[self.type][1] == type_last_char

    def compile(self) -> LexerResultT:
        return self._apply_type()

    def _apply_type(self):
        gen = (lemma.compile() if isinstance(lemma, Expression) else lemma
               for lemma in self.lemmas)
        return self.types[self.type][0](gen)

    def sub_ns(self, type_first_char: str) -> "Expression":
        return self.append(Expression(type_first_char=type_first_char))


DIVIDERS = ' \t\n'


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
