import pytest
import re
from contextlib import nullcontext as does_not_rise

from src.utils import top_10_salary, without_experience, remote_job, for_students, more_salary

@pytest.fixture
def vacancies_list():
    with open('src/../tests/vacancies_test.txt', 'r', encoding='utf-8') as file:
        return file.readlines()


class TestUtils:
    def test_top_10_salary(self, vacancies_list):
        res_list = top_10_salary(vacancies_list)
        max_salary = int(re.search(r'(\d{1,6}) руб', res_list[0]).group(1))
        min_salary = int(re.search(r'(\d{1,6}) руб', res_list[-1]).group(1))
        assert max_salary == 400000 and min_salary == 160000 and len(res_list) == 10

    def test_without_experience(self, vacancies_list):
        res_list = without_experience(vacancies_list)
        assert len(res_list) == 3

    def test_remote_job(self, vacancies_list):
        res_list = remote_job(vacancies_list)
        assert len(res_list) == 7

    def test_for_students(self, vacancies_list):
        res_list = for_students(vacancies_list)
        assert len(res_list) == 2

    @pytest.mark.parametrize(
        'salary, res, expectation',
        [
            ('50000', 17, does_not_rise()),
            ('150000', 11, does_not_rise()),
            ('250000', 5, does_not_rise()),
            ('qwerty', None, pytest.raises(ValueError))
        ]
    )
    def test_more_salary(self, salary, res, expectation, vacancies_list):
        with expectation:
            res_list = more_salary(vacancies_list, salary)
            assert len(res_list) == res
