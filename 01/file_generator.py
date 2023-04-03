from typing import List, Iterator, TextIO, Union
from io import TextIOBase


def search_lines(file: Union[TextIO, str], words: List[str]) -> Iterator[str]:
    if not isinstance(words, list):
        raise TypeError
    else:
        if not all(isinstance(elem, str) for elem in words):
            raise TypeError

    if not isinstance(file, TextIOBase) and not isinstance(file, str):
        raise TypeError

    if isinstance(file, str):
        f = open(file, 'r')
    else:
        f = file

    for line in f:
        for word in words:
            if word.lower() in line.lower().split():
                yield line.rstrip('\n')
                break

    if isinstance(file, str):
        f.close()
