from typing import List, Iterator, TextIO
from io import TextIOBase


def search_lines(file: TextIO, words: List[str]) -> Iterator[str]:
    if not isinstance(words, list):
        raise TypeError
    else:
        if not all(isinstance(elem, str) for elem in words):
            raise TypeError

    if not isinstance(file, TextIOBase):
        raise TypeError

    for line in file:
        for word in words:
            if word.lower() in line.lower().split():
                yield line.rstrip('\n')
                break
