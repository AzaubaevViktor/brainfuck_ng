import os

import pytest

from bytecode import ByteCode
from executor import Executor, ExecutorError
from interpreter import Interpreter
from lexer import FileSource, do_lex, Lemma, LexerResultT, StringLemma

files = [os.path.join("examples", name) for name in os.listdir("examples") if name.endswith(".bfh")]


@pytest.mark.parametrize('file_name', files)
def test_example(file_name):
    memory_check = [None] * 10
    out_check = None

    def _parse_addr(lemma: Lemma):
        return int(lemma.text[1:])

    def hbf_add(addr_: Lemma, value_: LexerResultT, executor):
        addr = _parse_addr(addr_)
        value = executor(value_)

        result = ""
        result += ">" * addr
        result += ("+" if value > 0 else "-") * abs(value)
        result += "<" * addr

        return result

    def hbf_print(addr_: Lemma, executor):
        addr = _parse_addr(addr_)

        result = ""
        result += ">" * addr
        result += "."
        result += "<" * addr
        return result

    def hbf_cycle(addr_: Lemma, commands: LexerResultT, executor):
        addr = _parse_addr(addr_)
        result = ">" * addr
        result += "["
        result += "<" * addr

        for item in commands:
            result += executor(item)

        result += ">" * addr
        result += "]"
        result += "<" * addr
        return result

    def hbf_check_mem(addr_: Lemma, value_: LexerResultT, executor):
        addr = _parse_addr(addr_)
        value = executor(value_)

        memory_check[addr] = value

    def hbf_check_out(text: StringLemma, executor):
        assert isinstance(text, StringLemma)

        nonlocal out_check
        if out_check is None:
            out_check = ""

        out_check += text.text

    def do_add(*values: LexerResultT, executor):
        return sum(map(executor, values))

    variables = {
        '@add': hbf_add,
        '@print': hbf_print,
        "@cycle": hbf_cycle,
        '@@mem': hbf_check_mem,
        '@@out': hbf_check_out,
        "+": do_add,
    }

    executor = Executor(variables)

    source = FileSource(file_name)
    lex_result = do_lex(source)

    try:
        results = [
            executor(item)
            for item in lex_result
        ]
    except ExecutorError as e:
        print(e.pretty())
        raise

    program_raw = "".join(item for item in results if item)
    print(program_raw)

    code = ByteCode(program_raw)
    interpreter = Interpreter(code)

    interpreter()

    for calc, expected in zip(interpreter.mem, memory_check):
        if expected is not None:
            assert calc == expected

    if out_check:
        assert interpreter.out == out_check






