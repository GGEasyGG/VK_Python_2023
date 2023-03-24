from __future__ import annotations
from typing import Union, List, Tuple


class CustomList(list):
    def __init__(self, arg: Union[List[Union[int, float]], Tuple[Union[int, float], ...]]) -> None:
        if not isinstance(arg, (list, tuple)):
            raise TypeError('CustomList can be created only based on a list or a tuple')
        else:
            if all(isinstance(elem, (int, float)) for elem in arg):
                super().__init__(arg)
            else:
                raise TypeError('CustomList elements must be of type int or float')

    def __add__(self, other: Union[CustomList, List]) -> CustomList:
        if not isinstance(other, (CustomList, list)):
            raise TypeError('Only the CustomList and default list can be added to the CustomList')

        if not all(isinstance(elem, (int, float)) for elem in other):
            raise TypeError('Only default list with elements of int or float type can be added to the CustomList')

        if len(self) < len(other):
            new_list = list(self)
            new_list.extend([0] * (len(other) - len(self)))
            result = CustomList([new_list[i] + other[i] for i in range(len(other))])
        elif len(self) > len(other):
            new_list = list(other)
            new_list.extend([0] * (len(self) - len(other)))
            result = CustomList([new_list[i] + self[i] for i in range(len(self))])
        else:
            result = CustomList([other[i] + self[i] for i in range(len(self))])

        return result

    def __radd__(self, other: Union[CustomList, List]) -> CustomList:
        return self + other

    def __sub__(self, other: Union[CustomList, List]) -> CustomList:
        if not isinstance(other, (CustomList, list)):
            raise TypeError('Only the CustomList and default list can be subtracted with the CustomList')

        if not all(isinstance(elem, (int, float)) for elem in other):
            raise TypeError('Only default list with elements of int or float type can be subtracted with the CustomList')

        if len(self) < len(other):
            new_list = list(self)
            new_list.extend([0] * (len(other) - len(self)))
            result = CustomList([new_list[i] - other[i] for i in range(len(other))])
        elif len(self) > len(other):
            new_list = list(other)
            new_list.extend([0] * (len(self) - len(other)))
            result = CustomList([self[i] - new_list[i] for i in range(len(self))])
        else:
            result = CustomList([self[i] - other[i] for i in range(len(self))])

        return result

    def __rsub__(self, other: Union[CustomList, List]) -> CustomList:
        return CustomList([(-1) * elem for elem in self - other])

    def __eq__(self, other: CustomList) -> bool:
        if not isinstance(other, CustomList):
            raise TypeError('Only the CustomList can be compared')

        if sum(self) != sum(other):
            return False
        else:
            return True

    def __ne__(self, other: CustomList) -> bool:
        return not self == other

    def __lt__(self, other: CustomList) -> bool:
        if not isinstance(other, CustomList):
            raise TypeError('Only the CustomList can be compared')

        if sum(self) < sum(other):
            return True
        else:
            return False

    def __ge__(self, other: CustomList) -> bool:
        return not self < other

    def __gt__(self, other: CustomList) -> bool:
        return (self >= other) and (self != other)

    def __le__(self, other: CustomList) -> bool:
        return not self > other

    def __str__(self) -> str:
        return f'{super().__str__()}, {sum(self)}'
