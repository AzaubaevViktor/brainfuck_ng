from typing import List, Optional

from ._types import ExpressionT


class LexerError(Exception):
    def __init__(self, ns_stack: List[ExpressionT] = None):
        self.ns_stack: Optional[List[ExpressionT]] = ns_stack

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.ns_stack}>"
