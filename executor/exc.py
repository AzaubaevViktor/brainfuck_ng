from typing import Union, List

from lexer import LexerResultT, Lemma


class ErrorStackFrame:
    def __init__(self, lemma: LexerResultT):
        self.lemma = lemma

    def __str__(self, wrong_lemma: LexerResultT = None):
        if not self.lemma:
            return "()"

        if isinstance(self.lemma, Lemma):
            s = f"{self.lemma.source}:{self.lemma.line}:{self.lemma.pos}: "
            show = " " * len(s)

            item = f"{self.lemma.text}"
            s += item
            if self.lemma == wrong_lemma:
                show += "^" * len(item)
            else:
                show += " " * len(item)

            if wrong_lemma:
                s += "\n" + show
            return s

        first: Lemma = self.lemma[0]
        s = f"{first.source}:{first.line}:{first.pos}: ("
        show = " " * len(s)

        for lemma in self.lemma:
            if isinstance(lemma, tuple):
                item = "(...)"
            else:
                item = lemma.text

            s += item

            if lemma == wrong_lemma:
                show += "^" * len(item)
            else:
                show += " " * len(item)

            if lemma is not self.lemma[-1]:
                s += " "
                show += " "

        s += ")"
        show += " "

        if wrong_lemma and show.strip():
            s += "\n" + show
        return s

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.lemma}>"


class ExecutorError(Exception):
    def __init__(self, msg, stack_frame: ErrorStackFrame = None):
        self.msg = msg
        self.stack_frames: List[ErrorStackFrame] = []
        if stack_frame:
            self.append(stack_frame)

    def append(self, stack_frame: Union[LexerResultT, ErrorStackFrame]):
        if not isinstance(stack_frame, ErrorStackFrame):
            stack_frame = ErrorStackFrame(stack_frame)

        self.stack_frames.append(stack_frame)

    def pretty(self):
        items = []

        wrong = self.stack_frames[0]

        for item in self.stack_frames:
            items.append(item.__str__(wrong.lemma))
            wrong = item

        items = [
            "Stack trace:",
            *items[::-1],
            f"Error msg: {self.msg}",
        ]

        return "\n".join(items)


class PythonExecutorError(ExecutorError):
    def __init__(self, orig_exc):
        msg = f"Python exception was captured: `{orig_exc}`"
        super(PythonExecutorError, self).__init__(msg)
