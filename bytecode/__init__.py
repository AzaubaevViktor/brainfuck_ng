from enum import Enum
from typing import List, Tuple


class ByteCodeError(Exception):
    pass


class WrongChar(ByteCodeError):
    pass


class MissingOpenCycle(ByteCodeError):
    pass


class UnknownByteCode(ByteCodeError):
    pass


class ByteCode:
    MEM = 0
    POS = 1
    PRINT = 2
    READ = 3
    CYCLE_START = 4
    CYCLE_STOP = 5

    def __init__(self):
        self.items: List[Tuple[int, int]] = []
        self.cycle_stack = []

    def __iadd__(self, other: str):
        for ch in other:
            self._add(ch)

        return self

    def _add(self, ch: str):
        assert len(ch) == 1

        opcode = None
        value = None

        if ch in ['+', '-']:
            opcode = self.MEM
            value = 1 if ch == '+' else -1
        if ch in ['<', '>']:
            opcode = self.POS
            value = 1 if ch == '>' else -1
        if ch == '.':
            opcode = self.PRINT
            value = 1
        if ch == ',':
            opcode = self.READ
            value = 1
        if ch == '[':
            opcode = self.CYCLE_START
        if ch == ']':
            opcode = self.CYCLE_STOP

        if opcode is None:
            raise WrongChar(ch)

        self._add_opcode(opcode, value)

    def _add_opcode(self, opcode, value: int):

        if opcode in (self.MEM, self.POS, self.PRINT, self.READ):
            last_opcode, last_value = self.items.pop() if self.items else (None, None)

            if last_opcode == opcode:
                self.items.append((opcode, last_value + value))
            else:
                if last_opcode is not None:
                    self.items.append((last_opcode, last_value))
                self.items.append((opcode, value))
        else:
            if opcode == self.CYCLE_START:
                self.cycle_stack.append(len(self.items))
                self.items.append((opcode, None))
            elif opcode == self.CYCLE_STOP:
                if not self.cycle_stack:
                    raise MissingOpenCycle()

                index = self.cycle_stack.pop()
                assert self.items[index] == (self.CYCLE_START, None)
                self.items[index] = (self.CYCLE_START, len(self.items))
                self.items.append((opcode, index))
            else:
                raise UnknownByteCode(opcode)
