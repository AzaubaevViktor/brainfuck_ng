import pytest

from bytecode import ByteCode
from interpreter import WrongPosition, Mem

items_check_generator = [
    ("+>" * count, [1] * count + [0] * 1000)
    for count in range(int(Mem.CHUNK * 3.5))
]


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
    interpreter = Interpreter()
    code = ByteCode(prg)

    if isinstance(mem, Exception):
        with pytest.raises(mem):
            interpreter(code)
    else:
        interpreter(code)

        for calc, expected in zip(interpreter.mem, mem):
            assert calc == expected


@pytest.mark.parametrize('prg, out', (
        ("+" * ord('a') + ".", "a"),
        ("+" * ord('A') + ".", "A"),
        ("+" * ord('a') + "..", "aa"),
        ("+" * ord('a') + ".+.+.", "abc"),
        ("+" * ord('A') + ".+.+.", "ABC"),
        ("+" * ord('a') + ">+++[<.>-]", "aaa"),
))
def test_out(prg, out):
    interpreter = Interpreter()
    code = ByteCode(prg)

    interpreter(code)

    assert interpreter.out == out
