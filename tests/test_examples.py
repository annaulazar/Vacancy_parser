import pytest
from contextlib import nullcontext as does_not_rise

from src.examples import A, Calculator

# def test_example1():
#     assert 1 == 1
#
#
# def test_main():
#     assert A.x == 1

class TestCalculator:
    @pytest.mark.parametrize(
        "x, y, res, expectation",
        [
            (1, 2, 0.5, does_not_rise()),
            (5, -1, -5, does_not_rise()),
            (5, '-1', None, pytest.raises(TypeError)),
            (5, 0, None, pytest.raises(ZeroDivisionError)),
            (0, 5, 0, does_not_rise()),
            (5, '0', None, pytest.raises(TypeError))

        ]
    )
    def test_devision(self, x, y, res, expectation):
        with expectation:
            assert Calculator().devide(x, y) == res


    @pytest.mark.parametrize(
        "x, y, res, expectation",
        [
            (1, 2, 3, does_not_rise()),
            (5, -1, 4, does_not_rise()),
            ('a', 'b', None, pytest.raises(TypeError))

        ]
    )
    def test_add(self, x, y, res, expectation):
        with expectation:
            assert Calculator().add(x, y) == res
