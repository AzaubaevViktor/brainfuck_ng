import pytest

from bytecode import ByteCode
from interpreter import WrongPosition, Mem, Interpreter

items_check_generator = [
    ("+>" * count, [1] * count + [0] * 1000)
    for count in range(int(Mem.CHUNK * 3.5))
]


_debug_bc = {
    ByteCode.MEM: '+',
    ByteCode.POS: ">",
    ByteCode.PRINT: ".",
    ByteCode.READ: ",",
    ByteCode.CYCLE_START: "[",
    ByteCode.CYCLE_STOP: "]"
}


def _debug(step: int, code: ByteCode, CP: int, mem: Mem, MP: int, out: str):
    print(">>", step, f"CP: {CP}; MP: {MP}")

    for index_, item in enumerate(code.items):
        s = f"{_debug_bc[item[0]]}:{item[1]}"
        if index_ == CP:
            s = f"{{{s}}}"
        else:
            s = f" {s} "

        print(s, end="")
    print()

    for index_, item in enumerate(mem.data):
        s = f"{item:3}"
        if index_ == CP:
            s = f"{{{s}}}"
        else:
            s = f" {s} "

        print(s, end="")
    print()


@pytest.mark.parametrize('prg, mem', (
        ("", [0, 0, 0]),
        ("+", [1]),
        ("-", [255]),
        (">+", [0, 1]),
        ("<", WrongPosition),
        (">>+<+", [0, 1, 1]),
        ("++[>++<-]", [0, 4]),
        ("->->->--.+>-.++", [255, 255, 255, 255, 1]),
        *items_check_generator
))
def test_mem(prg, mem):
    code = ByteCode(prg)
    interpreter = Interpreter(code)

    if isinstance(mem, type) and issubclass(mem ,Exception):
        with pytest.raises(mem):
            interpreter()
    else:
        interpreter(debug=_debug)

        for calc, expected in zip(interpreter.mem, mem):
            assert calc == expected


hello_programm = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+."


@pytest.mark.parametrize('prg, out', (
        ("+" * ord('a') + ".", "a"),
        ("+" * ord('A') + ".", "A"),
        ("+" * ord('a') + "..", "aa"),
        ("+" * ord('a') + ".+.+.", "abc"),
        ("+" * ord('A') + ".+.+.", "ABC"),
        ("+" * ord('a') + ">+++[<.>-]", "aaa"),
        (hello_programm, "Hello World!")
))
def test_out(prg, out):
    code = ByteCode(prg)
    interpreter = Interpreter(code)

    interpreter(debug=_debug)

    assert interpreter.out == out
