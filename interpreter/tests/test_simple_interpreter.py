import pytest

from bytecode import ByteCode
from interpreter import WrongPosition, Mem, Interpreter
from interpreter.tests.conftest import debug_interpreter_step

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
    code = ByteCode(prg)
    interpreter = Interpreter(code)

    if isinstance(mem, type) and issubclass(mem ,Exception):
        with pytest.raises(mem):
            interpreter()
    else:
        interpreter(debug=debug_interpreter_step)

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

    interpreter(debug=debug_interpreter_step)

    assert interpreter.out == out
