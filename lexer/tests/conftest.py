from typing import Callable, Any


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