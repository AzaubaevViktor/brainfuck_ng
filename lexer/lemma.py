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
        return f"<Lemma:{self.source}:{self.line}:{self.pos} `{self.text}`>"
