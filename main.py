from classes import *
from utils import *


headers = {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/105.0.0.0 Safari/537.36'
        }

with open('vacancies.txt', 'w', encoding='utf-8') as file:
    file.write('')
print('Подбираем вакансии на сайтах Superjob и hh.ru\nВведите ключевое слово для поиска')
user_input = input('<<< ').strip().lower()
print('Подбираем вакасии ...')
requests = Superjob(headers), Hh(headers)
count = 0
for request in requests:
    vacancies = request.get_request(user_input)
    count += len(vacancies)
    with open('vacancies.txt', 'a', encoding='utf-8') as file:
        file.write('\n'.join(vacancies) + '\n')
# count = 250

print(f'Найдено {count} вакансий')
while True:
    print('-' * 40)
    print('Выберите критерии отбора:\n1. Топ-10 самых высокооплачиваемых вакансий\n2. Вакансии без опыта работы.\n'
                  '3. Вакансии с удаленной работой.\n4. Вакансии для студентов.\n5. Вакансии с зарплатой больше '
          'заданной\n6. Выйти из программы.')
    print('-' * 40)

    functions = {'1': top_10_salary, '2': without_experience, '3': remote_job,
                 '4': for_students, '5': more_salary}
    user_choice = input('<<< ')
    if user_choice == '6':
        quit()
    with open('vacancies.txt', 'r', encoding='utf-8') as file:
        try:
            result = functions[user_choice](file)
            print(f'Под ваш запрос найдено {len(result)} вакансий\n')
            for item in result[:10]:
                print_vacancy(item)
            if len(result) > 10:
                answer = input('Показать все (Y/N)? <<< ').strip().lower()
                if answer == 'y':
                    for item in result[10:]:
                        print_vacancy(item)
        except KeyError:
            print('Введите число от 1 до 6')

