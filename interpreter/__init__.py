from typing import Optional

from bytecode import ByteCode


class WrongPosition(Exception):
    pass


class Mem:
    CHUNK = 16

    def __init__(self):
        self.data = []

    def __getitem__(self, index):
        if len(self.data) <= index:
            return 0

        return self.data[index]

    def __setitem__(self, index, value):
        while index >= len(self.data):
            self.data += [0] * self.CHUNK

        self.data[index] = value

    def __iter__(self):
        yield from self.data
        while True:
            yield 0


class Interpreter:
    def __init__(self, code: ByteCode, inp: Optional[str] = None):
        self.mem = Mem()
        self.code = code
        self._step = 0
        self.CP = 0
        self.MP = 0
        self.out = ""
        self.inp = iter(inp or "")

    def __call__(self, debug=None):
        if debug:
            debug(self._step, self.code, self.CP, self.mem, self.MP, self.out)

        while self.CP < len(self.code):
            self.step()
            if debug:
                debug(self._step, self.code, self.CP, self.mem, self.MP, self.out)

    def step(self):
        opcode, value = self.code[self.CP]

        if opcode == ByteCode.MEM:
            self.mem[self.MP] += value
            self.mem[self.MP] %= 256
        elif opcode == ByteCode.POS:
            self.MP += value
        elif opcode == ByteCode.PRINT:
            self.out += chr(self.mem[self.MP]) * value
        elif opcode == ByteCode.READ:
            for _ in range(value):
                self.mem[self.MP] = ord(next(self.inp))
        elif opcode == ByteCode.CYCLE_START:
            if self.mem[self.MP] == 0:
                self.CP = value
            else:
                self.CP += 1
        elif opcode == ByteCode.CYCLE_STOP:
            if self.mem[self.MP] != 0:
                self.CP = value
            else:
                self.CP += 1

        if opcode not in (ByteCode.CYCLE_START, ByteCode.CYCLE_STOP):
            self.CP += 1

        self._step += 1

        if self.MP < 0:
            raise WrongPosition(self.MP)

        if self.CP < 0:
            raise ValueError()
