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


class FileSource:
    CHUNK = 1024

    def __init__(self, file_name: str):
        self.file_name = file_name

    def __iter__(self):
        with open(self.file_name, "rt") as f:
            while data := f.read(self.CHUNK):
                yield from data

    def __repr__(self):
        return f"<FileSource:{self.file_name}>"
