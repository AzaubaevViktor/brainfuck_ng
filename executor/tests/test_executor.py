import pytest

from executor.exc import ExecutorError
from executor.tests.module_for_test import Main
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

checks = [
    ("hello", "world"),
    ("(append x) (append  y) (ret)", [('x', 'x_value'), ('y', 'y_value')]),
    ("10", 10),
    ("(int 10)", 10),
    ("(int -10)", -10),
    ("(int 1234)", 1234),
    ("(add (int 1) (int 2))", 3),
    ("(defn test [a b] ( (add a b) )) (test (int 1) (int 2))", 3),
    ("(defn test [a b] ( (add (int 1) a b) (add a b) )) (test (int 1) (int 2))", 3),
    ("(set new_var (int 1)) new_var", 1),
    ("(set check (int 1))"
     "(append check)"
     "(defn test [a] ("
     "    (set check a)"
     "    (append check)"
     "))"
     "(append check)"
     "(test (int 2))"
     "(append check)"
     "(ret)", [('check', 1), ('check', 1), ('check', 2), ('check', 1)]),
    ("(import at)"
     "(append some_text)"
     "(append (some_method (int 2) (int 3)))"
     "(ret)", [('some_text', Main.some_text), (tuple, 2 ** 3)]),
    # TODO: Test for module shutdown
    ('[1 2 3]', [1, 2, 3]),
    ('[1 2 "x" (add 5 10) ((op pow) 2 3)]', [1, 2, 'x', 15, 8]),
    ('((op pow) (int 2) (int 3))', 8),
    ('((op pow) 2 3)', 8),
    *string_values_tests,
    ('(append ((op add) "a" "b"))'
     '(ret)', [(tuple, "ab")]),
    ('(= check ((op getitem) "abcde" 2))'
     '(append check) (ret)', [('check', 'c')]),
    *dividers_tests
]


@pytest.mark.parametrize('programm, expected', checks)
def test_executor(executor, programm, expected):
    lex_result = do_lex(programm)
    result = executor(*lex_result)
    print(result)
    assert expected == result


wrongs = [
    ("un_kn", [("un_kn", "unknown", "variable")]),
    ("(add un_nk 1)", ["add", ("un_kn", "unknown", "variable")]),
    ("(defn func_name [arg1 arg2] ())"
     "(func_name 12)", [("func_name", "arg2")]),
    ("(defn func_name [arg1] ())"
     "(func_name 12 12)", [("func_name", "too many", "arg1")]),
    ("(defn func_name [arg1] ("
     "   (add 10 unk_nown)"
     "))", ["func_name", 'add', "unk_nown"])
]


@pytest.mark.parametrize('program, stack', wrongs)
def test_wrong_input(executor, program, stack):
    lex_result = do_lex(program)
    with pytest.raises(ExecutorError) as exc_info:
        executor(*lex_result)

    e: ExecutorError = exc_info.value
    for expected, stack_frame in zip(stack, e.stack_frames):
        if not isinstance(expected, tuple):
            expected = (expected, )

        for item in expected:
            assert item in str(stack_frame)
