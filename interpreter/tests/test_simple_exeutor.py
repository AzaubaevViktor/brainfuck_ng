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


def _print_items(items, current, fmt='{{{}}}', fmt_item='{}'):
    for index_, item_ in enumerate(items):
        item = fmt_item.format(item_)

        if index_ - 1 == current:
            s = f" {item}"
        elif index_ + 1 == current:
            s = f"{item} "
        elif index_ == current:
            s = fmt.format(item)
        else:
            s = f" {item} "

        print(s, end='')
    print()


def _debug(step: int, code: ByteCode, CP: int, mem: Mem, MP: int, out: str):
    print(">>", step, f"CP: {CP}; MP: {MP}")

    _print_items(code.items, CP, fmt_item="{0[0]}:{0[1]}")
    _print_items(mem.data, MP, fmt_item="{:3}")
    print(out)


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
