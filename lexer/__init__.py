from typing import Iterable, Union, List, Sequence


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


LemmaT = Union[Lemma, "NameSpace"]


class NameSpace:
    types = {
        '(': (tuple, ')'),
        '[': (list, ']'),
    }

    def __init__(self, type_: str = None, lemmas: Sequence[LemmaT] = None):
        self.type = None
        if type_:
            self.set_type(type_)
        self.lemmas: List[LemmaT] = list(lemmas or [])

    def append(self, item: Union[Lemma, "NameSpace"]):
        self.lemmas.append(item)
        return item

    def set_type(self, char):
        if char not in self.types:
            raise LexerError(char)
        self.type = char

    def check_type(self, char):
        assert self.types[self.type][1] == char

    def compile(self):
        gen = (lemma.compile if isinstance(lemma, NameSpace) else lemma
               for lemma in self.lemmas)

        return self.types[self.type][0](gen)

    def sub_ns(self, type_: str) -> "NameSpace":
        return self.append(NameSpace(type_=type_))


DIVIDERS = ' \t\n'


def do_lex(source: Union[BaseSource, str]):
    if isinstance(source, str):
        source = StringSource(source)

    root_obj = NameSpace()
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

        if symbol in ('(', ']'):
            if isinstance(current, Lemma):
                raise NotImplementedError()
            else:
                ns_stack.append(current.sub_ns(symbol))
        elif symbol in (')', ']'):
            if isinstance(current, Lemma):
                raise NotImplementedError()
            else:
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
