from typing import Union

from lexer import LexerResultT, Lemma


class ErrorStackFrame:
    def __init__(self, lemma: LexerResultT):
        self.lemma = lemma

    def __str__(self):
        if isinstance(self.lemma, Lemma):

            return f"{self.lemma.source}:{self.lemma.line}:{self.lemma.pos}: {self.lemma.text}"

        first: Lemma = self.lemma[0]
        s = f"{first.source}:{first.line}:{first.pos}: ("
        for lemma in self.lemma:
            if isinstance(lemma, tuple):
                s += "(...)"
            else:
                s += lemma.text

            if lemma is not self.lemma[-1]:
                s += " "

        s += ")"

        return s

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.lemma}>"


class ExecutorError(Exception):
    def __init__(self, msg, stack_frame: ErrorStackFrame = None):
        self.msg = msg
        self.stack_frames = []
        if stack_frame:
            self.append(stack_frame)

    def append(self, stack_frame: Union[LexerResultT, ErrorStackFrame]):
        if not isinstance(stack_frame, ErrorStackFrame):
            stack_frame = ErrorStackFrame(stack_frame)

        self.stack_frames.append(stack_frame)

    def pretty(self):
        s = "Stack trace:\n"
        for item in self.stack_frames[::-1]:
            s += f"{item}\n"

        s += f"Error msg: {self.msg}\n"

        return s
