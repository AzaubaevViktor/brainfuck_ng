from typing import Iterable


class BaseSource:
    def __iter__(self) -> Iterable[str]:
        raise NotImplementedError()


class StringSource:
    def __init__(self, data: str):
        self.data = data

    def __iter__(self):
        yield from self.data

    def __repr__(self):
        return f"<StrSource({len(self.data)})>"
