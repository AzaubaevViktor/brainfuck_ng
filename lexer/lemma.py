from .sources import BaseSource


class Lemma:
    def __init__(self, source: BaseSource, text: str, line: int, pos: int):
        self.source = source
        self.text = text
        self.line = line
        self.pos = pos

    def append(self, ch):
        self.text += ch

    def __eq__(self, other: 'Lemma'):
        if not isinstance(other, Lemma):
            return False

        return (self.source == other.source
                and self.text == other.text
                and self.line == other.line
                and self.pos == other.pos)

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.source}:{self.line}:{self.pos} `{self.text}`>"


class StringLemma(Lemma):
    ECSAPES = {
        'n': '\n',
        't': '\t',
        '\\': '\\\\',
        '"': '"'
    }

    def __init__(self, source: BaseSource, text: str, line: int, pos: int):
        super().__init__(source, text, line, pos)
        self.finished = False
        self.escaping = False

    def process_escape(self, char: str) -> str:
        self.escaping = False
        self.text += self.ECSAPES[char]

