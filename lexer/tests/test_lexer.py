from typing import Callable, Any

import pytest

from lexer import do_lex

checks = [
    ("", tuple()),
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
        if isinstance(lex, tuple) and isinstance(result, tuple):
            assert check_correct(lex, res, check)
        else:
            assert check(lex, res)

    return True


@pytest.mark.parametrize('source, result', checks)
def test_lexer(source, result):
    assert check_correct(do_lex(source), result, lambda lex, res: lex.text == res)
