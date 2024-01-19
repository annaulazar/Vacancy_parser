#  Тестовый код для тренировки pytest
from typing import Union


class A:
    x = 1


class Calculator:
    def devide(self, x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
        return x / y

    def add(self, x: Union[int, float], y: Union[int, float]) -> Union[int, float]:
        return x + y

