from classes import *


headers = {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/105.0.0.0 Safari/537.36'
        }



with open('vacancies.txt', 'w', encoding='utf-8') as file:
    file.write('')

user_input = 'python'

requests = Superjob(headers), Hh(headers)

for request in requests:
    vacancies = request.get_request(user_input)
    with open('vacancies.txt', 'a', encoding='utf-8') as file:
        file.write('\n'.join(vacancies) + '\n')

