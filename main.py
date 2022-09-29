from classes import *
from utils import *
from fake_useragent import UserAgent


def get_vacancies() -> int:
    """
    Функция получает по запросам вакансии с двух сайтов и записывает их в файл в виде строк
    :return: количество найденных вакансий
    """
    headers = {
                'accept': '*/*',
                'user-agent': UserAgent().opera
            }
    with open('vacancies.txt', 'w', encoding='utf-8') as file:
        file.write('')
    print('Подбираем вакансии на сайтах Superjob и hh.ru\nВведите ключевое слово для поиска')
    user_input = input('<<< ').strip().lower()
    print('Подбираем вакасии ...')
    my_requests = Superjob(headers), Hh(headers)  # Создаем объекты классов запросов
    count_vacancies = 0
    failure = False  # Флаг, что уже с одного сайта был отказ
    for req in my_requests:
        try:
            vacancies = req.get_request(user_input)
            count_vacancies += len(vacancies)
            with open('vacancies.txt', 'a', encoding='utf-8') as file:
                file.write('\n'.join(vacancies) + '\n')
        except Exception as ex:
            print(f'Сайт {req.name} не отвечает, {ex}')
            if failure:
                print('Попробуйте позднее')  # Завершаем программу, если отказ с двух сайтов
                quit()
            failure = True
    return count_vacancies


def main() -> None:
    count = get_vacancies()
    print(f'Найдено {count} вакансий')
    while True:
        print('-' * 40)
        print('Выберите критерии отбора:\n1. Топ-10 самых высокооплачиваемых вакансий\n2. Вакансии без опыта работы.\n'
              '3. Вакансии с удаленной работой.\n4. Вакансии для студентов.\n5. Вакансии с зарплатой больше '
              'заданной\n6. Выйти из программы.')
        print('-' * 40)
        # словарь с функциями по номерам меню
        functions = {'1': top_10_salary, '2': without_experience, '3': remote_job,
                     '4': for_students, '5': more_salary}
        user_choice = input('<<< ')
        if user_choice == '6':
            quit()
        with open('vacancies.txt', 'r', encoding='utf-8') as file:
            try:
                result = functions[user_choice](file)
                print(f'Под ваш запрос найдено {len(result)} вакансий\n')
                for item in result[:10]:  # Сразу выводим только 10 подходящих вакансий, по запросу остальные
                    print_vacancy(item)
                if len(result) > 10:
                    answer = input('Показать все (Y/N)? <<< ').strip().lower()
                    if answer == 'y':
                        for item in result[10:]:
                            print_vacancy(item)
            except KeyError:
                print('Введите число от 1 до 6')


if __name__ == '__main__':
    main()
