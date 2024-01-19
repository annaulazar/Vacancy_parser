import pytest
from src.examples import A, Calculator

# def test_example1():
#     assert 1 == 1
#
#
# def test_main():
#     assert A.x == 1


@pytest.mark.parametrize(
    "x, y, res",
    [
        (1, 2, 0.5),
        (5, -1, -5),

    ]
)
def test_devision(x, y, res):
    assert Calculator().devide(x, y) == res


@pytest.mark.parametrize(
    "x, y, res",
    [
        (1, 2, 3),
        (5, -1, 4),

    ]
)
def test_add(x, y, res):
    assert Calculator().add(x, y) == res
