import os
from typing import Iterable


class BaseSource:
    def __iter__(self) -> Iterable[str]:
        raise NotImplementedError()

    def __eq__(self, other: "BaseSource"):
        raise NotImplementedError()


class StringSource:
    def __init__(self, data: str):
        self.data = data

    def __iter__(self):
        yield from self.data

    def __eq__(self, other: "BaseSource"):
        if not isinstance(other, StringSource):
            return False

        return self.data == other.data

    def __repr__(self):
        return f"<StrSource({len(self.data)})>"


class FileSource:
    CHUNK = 1024

    def __init__(self, file_name: str):
        self.file_name = file_name
        if not os.path.exists(self.file_name):
            raise FileNotFoundError(self.file_name)

    def __iter__(self):
        with open(self.file_name, "rt") as f:
            while data := f.read(self.CHUNK):
                yield from data

    def __eq__(self, other: BaseSource):
        if not isinstance(other, FileSource):
            return False

        return self.file_name == other.file_name

    def __repr__(self):
        return f"<FileSource:{self.file_name}>"
