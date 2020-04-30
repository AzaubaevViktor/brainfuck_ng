import pytest

from bytecode import ByteCode, ByteCodeError, MissingOpenCycle, WrongChar

items = (
    ("+++", [(ByteCode.MEM, 3)]),
    ("--", [(ByteCode.MEM, -2)]),
    (">>>>", [(ByteCode.POS, 4)]),
    ("<<<<<", [(ByteCode.POS, -5)]),
    ("<", [(ByteCode.POS, -1)]),
    ("..", [(ByteCode.PRINT, 2)]),
    (",,,", [(ByteCode.READ, 3)]),
    ("[+]", [(ByteCode.CYCLE_START, 2), (ByteCode.MEM, 1), (ByteCode.CYCLE_STOP, 0)]),
    ("+[+>]",
     [(ByteCode.MEM, 1), (ByteCode.CYCLE_START, 4), (ByteCode.MEM, 1), (ByteCode.POS, 1), (ByteCode.CYCLE_STOP, 1)]),
    ("[", [(ByteCode.CYCLE_START, None)]),
    (">>++<<--", [(ByteCode.POS, 2), (ByteCode.MEM, 2), (ByteCode.POS, -2), (ByteCode.MEM, -2)]),

)


@pytest.mark.parametrize(
    'line, op_codes', items
)
def test_simple(line, op_codes):
    bc = ByteCode()

    bc += line

    assert bc.items == op_codes


@pytest.mark.parametrize(
    'line, op_codes', items
)
def test_simple_init(line, op_codes):
    bc = ByteCode(line)

    assert bc.items == op_codes


@pytest.mark.parametrize(
    'line, op_codes', items
)
def test_simple_by_pos(line, op_codes):
    bc = ByteCode()

    for ch in line:
        bc += ch

    assert bc.items == op_codes


@pytest.mark.parametrize('char, error', (
        (']', MissingOpenCycle),
        ('?', WrongChar)
))
def test_wrong(char, error):
    bc = ByteCode()

    with pytest.raises(error):
        bc += char
