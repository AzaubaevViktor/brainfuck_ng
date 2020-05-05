import pytest

from executor.builtin.module_for_test import At
from executor.exc import ExecutorError
from lexer import do_lex, DIVIDERS

_dividers_raw = repr(DIVIDERS)[1:-1]

string_values_tests = [
    (f'(= test "{s}")'
     '(append test)'
     '(ret)', [('test', s)])
    for s in (
        "test",
        "a a a ",
        "( ha () ha ) ha ) ha )",
        "corova linux: 🦠",
        "💀\t🔥♷"
    )
]

dividers_tests = [
    (f"(= dividers \"{_dividers_raw}\")"
     f"(append ((op getitem) dividers {index}))"
     f"(ret)", [(tuple, DIVIDERS[index])])
    for index in range(len(DIVIDERS))
]

import_tests = [
    ("(import:builtin:inline at)"
     "(append some_text)"
     "(append (some_method (int 2) (int 3)))"
     "(ret)", [('some_text', At.some_text), (tuple, 2 ** 3)]),
    ("(import:builtin at)"
     "(append (. at some_text))"
     "(ret)", [(tuple, At.some_text)]),
    ("(import:builtin at ("
     "    (append some_text)"
     "    (append (some_method 2 3))"
     "))"
     "(ret)", [('some_text', At.some_text), (tuple, 2 ** 3)]),
    ('(import:inline "executor/tests/module.lsp")'
     "(append some_text)"
     "(append (mul_sum 2 3 5))"
     "(ret)", [('some_text', "text"), (tuple, 11)]),
    ('(import "executor/tests/module.lsp" ('
     "    (append some_text)"
     "    (append (mul_sum 2 3 5))"
     "))"
     "(ret)", [('some_text', "text"), (tuple, 11)]),
    ('(= module (import "executor/tests/module.lsp"))'
     "(append (. module some_text))"
     "(append ((. module mul_sum) 2 3 5))"
     "(ret)", [(tuple, "text"), (tuple, 11)])
]

checks = [
    ("hello", "world"),
    ("(append x) (append  y) (ret)", [('x', 'x_value'), ('y', 'y_value')]),
    ("10", 10),
    ("(int 10)", 10),
    ("(int -10)", -10),
    ("(int 1234)", 1234),
    ("(+ (int 1) (int 2))", 3),
    ("(defn test [a b] ( (+ a b) )) (test (int 1) (int 2))", 3),
    ("(defn test [a b] ( (+ (int 1) a b) (+ a b) )) (test (int 1) (int 2))", 3),
    ("(= new_var (int 1)) new_var", 1),
    ("(= check (int 1))"
     "(append check)"
     "(defn test [a] ("
     "    (= check a)"
     "    (append check)"
     "))"
     "(append check)"
     "(test (int 2))"
     "(append check)"
     "(ret)", [('check', 1), ('check', 1), ('check', 2), ('check', 1)]),
    # TODO: Test for module shutdown
    ('[1 2 3]', [1, 2, 3]),
    ('[1 2 "x" (+ 5 10) ((op pow) 2 3)]', [1, 2, 'x', 15, 8]),
    ('((op pow) (int 2) (int 3))', 8),
    ('((op pow) 2 3)', 8),
    *string_values_tests,
    ('(append ((op add) "a" "b"))'
     '(ret)', [(tuple, "ab")]),
    ('(= check ((op getitem) "abcde" 2))'
     '(append check) (ret)', [('check', 'c')]),
    *dividers_tests,
    *import_tests,
]


@pytest.mark.parametrize('programm, expected', checks)
def test_executor(executor, programm, expected):
    lex_result = do_lex(programm)
    try:
        result = executor(*lex_result)
    except ExecutorError as e:
        print(e.pretty())
        raise

    print(result)
    assert expected == result


wrongs = [
    ("un_kn", ["un_kn"], ("term", "not found", "un_kn")),
    ("(+ un_kn 1)", ["+", "un_kn"], ("un_kn", "not found", "term")),
    ("(defn func_name [arg1 arg2] ())"
     "(func_name 12)", ["func_name"], ("func_name", "arg2", "expect", "argument")),
    ("(defn func_name [arg1] ())"
     "(func_name 12 12)", ["func_name"], ("too many", "expect 1")),
    ("(defn func_name [arg1] ("
     "   (+ 10 unk_nown)"
     "))"
     "(func_name 10)", ["func_name", '+', 'unk_nown'], ("unk_nown", "not found", "term")),
    ("(import:builtin at)"
     "(append some_text)", ["append", "some_text"], ("not found", "term", "some_text")),
    ('(import "executor/tests/module.lsp")'
     "(mul_sum 2 3 5)", ['mul_sum'], ('not found', 'term', 'mul_sum')),
    ('(import "unknown/file.lsp")', ["import", "unknown/file.lsp"],
     ("does not", "exist", "module")),
    ('(import:builtin wrong_module)', ['import:builtin', "wrong_module"],
     ("does not found in builtin modules", "wrong_module")),
    ('(import "executor/tests/wrong.lsp")', ['import', 'print', 'unk_nown', 'unk_nown'],
     ("not found", "term", "unk_nown"))
]


@pytest.mark.parametrize('program, stack, msg', wrongs)
def test_wrong_input(executor, program, stack, msg):
    lex_result = do_lex(program)
    with pytest.raises(ExecutorError) as exc_info:
        executor(*lex_result)

    e: ExecutorError = exc_info.value

    print("~~ ~~ ~~ ~~ ~~ ~~ ~~")
    pretty = e.pretty()
    print(pretty)
    print()
    print("~~ ~~ ERROR ~~ ~~")
    print(exc_info.getrepr())
    print("-----------------")

    if not isinstance(msg, tuple):
        msg = (msg, )

    msg_lower = e.msg.lower()
    for msg_ in msg:
        assert msg_ in msg_lower

    for expected, stack_frame in zip(stack[::-1], e.stack_frames):
        print(stack_frame)
        if not isinstance(expected, tuple):
            expected = (expected, )

        lower_str = str(stack_frame).lower()

        for item in expected:
            assert item in lower_str


