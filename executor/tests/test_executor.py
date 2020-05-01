import pytest

from executor.tests.module_for_test import Main
from lexer import do_lex

checks = [
    ("hello", "world"),
    ("(append x) (append  y) (ret)", [('x', 'x_value'), ('y', 'y_value')]),
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
    # TODO: Test for shutdown
]


@pytest.mark.parametrize('programm, expected', checks)
def test_executor(executor, programm, expected):
    lex_result = do_lex(programm)
    result = executor(lex_result)
    print(result)
    assert expected == result
