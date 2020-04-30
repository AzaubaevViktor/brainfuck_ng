from typing import Iterable, Union, List


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


class Lemma:
    def __init__(self, source: BaseSource, text: str, line: int, pos: int):
        self.source = source
        self.text = text
        self.line = line
        self.pos = pos


class NameSpace:
    types = {
        '(': (tuple, ')'),
        '[': (list, ']'),
    }

    def __init__(self):
        self.type = None
        self.lemmas: List[Union[Lemma, NameSpace]] = []

    def append(self, item: Union[Lemma, "NameSpace"]):
        self.lemmas.append(item)

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


def do_lex(source: Union[BaseSource, str]):
    if isinstance(source, str):
        source = StringSource(source)

    root_obj = NameSpace()
    root_obj.set_type('(')

    for symbols in source:
        pass

    root_obj.check_type(')')

    return root_obj.compile()
