class ErrorStackFrame:
    pass


class ExecutorError(Exception):
    def __init__(self, msg, stack_frame: ErrorStackFrame):
        self.msg = msg
        self.stack_frames = [stack_frame]

    def append(self, stack_frame: ErrorStackFrame):
        self.stack_frames.append(stack_frame)
