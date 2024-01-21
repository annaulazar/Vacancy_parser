#  Тестовый код для тренировки pytest
from typing import Union


class A:
    x = 1


class Calculator:
    def devide(self, x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
        if not isinstance(x, (int, float)) or not isinstance(x, (int, float)):
            raise TypeError("Both arguments should be numeric")
        if y == 0:
            raise ZeroDivisionError("Cannot devide by zerro")
        return x / y

    def add(self, x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
        if not isinstance(x, (int, float)) or not isinstance(x, (int, float)):
            raise TypeError("Both arguments should be numeric")
        return x + y

