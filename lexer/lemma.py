from .sources import BaseSource


class Lemma:
    def __init__(self, source: BaseSource, text: str, line: int, pos: int):
        self.source = source
        self.text = text
        self.line = line
        self.pos = pos

    def append(self, ch):
        self.text += ch

    def __repr__(self):
        return f"<{self.__class__.__name__}:{self.source}:{self.line}:{self.pos} `{self.text}`>"


class StringLemma(Lemma):
    def __init__(self, source: BaseSource, text: str, line: int, pos: int):
        super().__init__(source, text, line, pos)
        self.finished = False
