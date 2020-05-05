from typing import Union

from lexer import LexerResultT


class ErrorStackFrame:
    def __init__(self, lemma: LexerResultT):
        self.lemma = lemma

    def __str__(self):
        return f"{self.lemma}"

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
        s = f"Error: {self.msg}\n"
        for item in self.stack_frames[::-1]:
            s += f"{item}\n"

        return s
