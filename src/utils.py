import re
from typing import Union


def top_10_salary(data: list) -> list:
    res = sorted(data, key=lambda x: -int(re.search(r'(\d{1,6}) руб', x).group(1)))[:10]
    return res


def without_experience(data: list) -> list:
    res = filter(lambda x: 'Опыт не нужен' in x, data)
    return list(res)


def remote_job(data: list) -> list:
    res = filter(lambda x: 'Удаленная работа' in x, data)
    return list(res)


def for_students(data: list) -> list:
    res = filter(lambda x: 'Доступно студентам' in x, data)
    return list(res)


def more_salary(data: list, user_salary: str) -> list:
    try:
        user_salary = int(user_salary)
    except ValueError:
        raise ValueError
    user_salary = int(user_salary)
    res = filter(lambda x: int(re.search(r'(\d{1,6}) руб', x).group(1)) >= user_salary, data)
    return list(res)


def print_vacancy(data: str) -> None:
    line = [x.strip() for x in data.split('|')]
    title = line[0]
    tag = line[1] if line[1] != 'None' else ''
    salary = line[2] if line[2] != '0 руб' else 'По договоренности'
    description = line[3]
    link = line[4]
    print('=' * 50)
    print(title, tag, salary, description, link, sep='\n')
    print()


def print_vacancies(result_list: list) -> None:
    print(f'Под ваш запрос найдено {len(result_list)} вакансий\n')
    for item in result_list[:10]:  # Сразу выводим только 10 подходящих вакансий, по запросу остальные
        print_vacancy(item)
    if len(result_list) > 10:
        answer = input('Показать все (Y/N)? <<< ').strip().lower()
        if answer == 'y':
            for item in result_list[10:]:
                print_vacancy(item)
