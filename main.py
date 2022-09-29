from classes import *


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

print(f'Найдено {count} вакансий')
print('-' * 40)
print('Выберите критерии отбора:\n1. Топ-10 самых высокооплачиваемых вакансий\n2. Вакансии без опыта работы.\n'
              '3. Вакансии с удаленной работой.\n4. Вакансии для студентов.\n5. Выйти из программы.')
print('-' * 40)

