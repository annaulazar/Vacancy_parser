import re


def top_10_salary(data) -> list:
    res = sorted(data, key=lambda x: -int(re.search(r'(\d{1,6}) руб', x).group(1)))
    return res[:10]


def without_experience(data) -> list:
    res = filter(lambda x: 'Опыт не нужен' in x, data)
    return list(res)


def remote_job(data) -> list:
    res = filter(lambda x: 'Удаленная работа' in x, data)
    return list(res)


def for_students(data) -> list:
    res = filter(lambda x: 'Доступно студентам' in x, data)
    return list(res)


def more_salary(data) -> list:
    print('Введите размер заработной платы')
    while True:
        user_salary = input('<<< ')
        try:
            user_salary = int(user_salary)
            res = filter(lambda x: int(re.search(r'(\d{1,6}) руб', x).group(1)) >= user_salary, data)
            return list(res)
        except ValueError:
            print('Введите число')
            continue


def print_vacancy(data) -> None:
    line = [x.strip() for x in data.split('|')]
    title = line[0]
    tag = line[1] if line[1] != 'None' else ''
    salary = line[2] if line[2] != '0 руб' else 'По договоренности'
    description = line[3] if line[3] != 'None' else 'Описания нет'
    link = line[4]
    print('=' * 50)
    print(title, tag, salary, description, link, sep='\n')
    print()




# file = ['Java-разработчик (Middle) | None | от 180000 руб | Участие в проектировании систем. Доработка существующих продуктов | https://russia.superjob.ru/vakansii/ml-inzhener-44342838.html',
#         'Java-разработчик | Удаленная работа | 100000 - 300000 руб | Улучшение и доработка существующего кода. | https://russia.superjob.ru/vakansii/ml-inzhener-44342838.html',
#         'Разработчик JAVA (монолит) | Удаленная работа | 0 руб | Разработка кода БД/<highlighttext | https://russia.superjob.ru/vakansii/ml-inzhener-44342838.html',
#         'Scala / Java Developer (senior) | None | 200000 - 300000 руб | Биллинговые системы. Системы и технологии процессинга | https://russia.superjob.ru/vakansii/ml-inzhener-44342838.html',
#         'Java developer | None | от 100000 руб | Разрабатывать программные продукты для конечного пользователя | https://russia.superjob.ru/vakansii/ml-inzhener-44342838.html',
#         'Инженер-программист java/C++ | Опыт не нужен | 50000 - 60000 руб | None | https://hh.ru/vacancy/70135639 | https://russia.superjob.ru/vakansii/ml-inzhener-44342838.html',
#         'ML инженер (computer vision и machine learning) | Доступно студентам | от 55000 руб. | Разработка методов | https://russia.superjob.ru/vakansii/ml-inzhener-44342838.html,']

# result = remote_job(file)
# print(f'Под ваш запрос найдено {len(result)} вакансий\n')
# for item in result:
#     print_vacancy(item)


# s = '55 000 — 75 000 руб.'
# s = s.split(' ')
# print(s)
# if 'от' in s or 'до' in s:
#     s = ' '.join((s[0], s[1] + s[2], s[3]))
# else:
#     s = ' '.join((s[0] + s[1], s[2] , s[3] + s[4], s[5]))
#
# print(s)