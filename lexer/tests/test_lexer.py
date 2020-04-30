from typing import Callable, Any

import pytest

from lexer import do_lex

checks = [
    ("", None),
    ("(a b c)", ('a', 'b', 'c')),
    ("( a b c)", ('a', 'b', 'c')),
    ("(a b c )", ('a', 'b', 'c')),
    ("(a b    c)", ('a', 'b', 'c')),
    ("(    a     b       c   )", ('a', 'b', 'c')),
    ("(a \nb    \n c\n\n\n\n)\n", ('a', 'b', 'c')),
    ("(a (b c))", ('a', ('b', 'c'))),
    ("(a [b c])", ('a', ['b', 'c'])),
    ("((a b) (c d (e f))", (('a', 'b'), ('c', 'd', ('e', 'f')))),
    ("(abcdef abcdef)", ("abcdef", "abcdef")),
    ("(print \"test\")", ("print", "\"test\"")),
    ("(print \"(lol man)\")", ("print", "\"(lol man)\"")),
    ("(print \"Oh my... \\\" god\"", ("print", "\"Oh my... \\\" god\""))
]


def check_correct(lexes, result, check: Callable[[Any, Any], bool]):
    assert len(lexes) == len(result)

    for lex, res in zip(lexes, result):
        if isinstance(lex, tuple) and isinstance(res, tuple):
            assert check_correct(lex, res, check)
        elif isinstance(lex, list) and isinstance(res, list):
            assert check_correct(lex, res, check)
        else:
            assert check(lex, res)

    return True


@pytest.mark.parametrize('source, expected_into', checks)
def test_lexer(source, expected_into):
    expected = (expected_into, ) if expected_into is not None else tuple()
    result = do_lex(source)
    assert check_correct(result, expected, lambda lex, res: lex.text == res)
