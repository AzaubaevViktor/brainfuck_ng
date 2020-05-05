import os

import pytest

from bytecode import ByteCode
from executor import Executor, ExecutorError
from executor.builtin import ModuleImporter
from interpreter import Interpreter
from lexer import FileSource, do_lex, Lemma, LexerResultT, StringLemma


def _files():
    for root, folders, files in os.walk("examples"):
        for file in files:
            if file.endswith(".bfh"):
                yield os.path.join(root, file)


files = tuple(_files())


@pytest.mark.parametrize('file_name', files)
def test_example(file_name):
    memory_check = [None] * 10
    out_check = None

    def _parse_addr(lemma: Lemma):
        return int(lemma.text[1:])

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

    variables = {
        '@@mem': hbf_check_mem,
        '@@out': hbf_check_out,
        **ModuleImporter.scope_with_import(),
    }

    executor = Executor(variables)

    try:
        from hbf.hbf_builtin import HBFBuiltin
        from modules.builtin import BaseBuiltin

        executor.run("(import:builtin:inline builtin)")
        executor.run("(import:builtin:inline hbf)")
        executor.run('(import:inline "hbf/hbf.lsp")')

        source = FileSource(file_name)
        lex_result = do_lex(source)

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






