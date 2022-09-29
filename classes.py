import requests as rq
import requests.exceptions
from bs4 import BeautifulSoup as BS
from abc import ABC, abstractmethod
from typing import Optional


class Engine(ABC):
    @abstractmethod
    def get_request(self, user_key):
        pass


class Superjob(Engine):

    def __init__(self, headers: dict) -> None:
        self.headers = headers
        self.name = 'Superjob'
        self.res = []

    def get_request(self, user_key: str) -> list:
        """
        Функция получает список вакансий с сайта Superjob по ключеому слову user_key
        """
        page = 1
        vacancies = '1'
        while len(vacancies) > 0:
            url = f'https://russia.superjob.ru/vacancy/search/?keywords={user_key}&page={page}'
            soup = BS(rq.get(url, headers=self.headers).text, 'lxml')
            vacancies = soup.find_all(class_='_8zbxf f-test-vacancy-item _3HN9U hi8Rr _3E2-y _1k9rz')
            for vacancy in vacancies:
                name = vacancy.find(class_="_9fIP1 _249GZ _1jb_5 QLdOc")
                title = name.text
                link = 'https://russia.superjob.ru' + name.find('a').get('href')
                salary = vacancy.find(class_='_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi').text
                description = vacancy.find(class_='_1Nj4W _249GZ _1jb_5 _1dIgi _3qTky').text
                tag = vacancy.find(class_='_3gyJS _1nh_W')
                if tag:
                    tag = tag.text
                self.res += [f'{title} / {tag} / {salary} / {description} / {link}']
            page += 1
        return self.res


class Hh(Engine):

    def __init__(self, headers: dict) -> None:
        self.headers = headers
        self.name = 'hh.ru'
        self.res = []

    def get_tag(self, dict_tags: dict) -> Optional[str]:
        """
        Функция из переданного словаря полей вакансии получает дополнительные теги ('Опыт не нужен' или 'Удаленная работа')
        """
        tags = []
        if dict_tags['remote'] == 'Удаленная работа':
            tags.append('Удаленная работа')
        if dict_tags['experience'] == 'Нет опыта':
            tags.append('Опыт не нужен')
        if not tags:
            return None
        return ' '.join(tags)

    def get_salary(self, salary_dict: dict) -> str:
        """
        Функция из переданного словаря зарплаты получает строку для единого представления
        """
        if salary_dict is None:
            return 'По договоренности'
        if salary_dict['currency'] == 'RUR':
            rate = 1
        else:
            rate = 60
        if salary_dict['from'] and salary_dict['to']:
            return f'{salary_dict["from"] * rate} - {salary_dict["to"] * rate} руб'
        if not salary_dict['to']:
            return f'от {salary_dict["from"] * rate} руб'
        return f'до {salary_dict["to"] * rate} руб'

    def get_request(self, user_key: str) -> list:
        """
        Функция получает список вакансий с сайта hh.ru по ключеому слову
        """
        url = 'https://api.hh.ru/vacancies'
        for i in range(1, 51):
            par = {"text": user_key, 'area': '113', 'per_page': '10', 'page': str(i)}
            response = requests.get(url, params=par, headers=self.headers).json()
            for item in response['items']:
                title = item['name']
                link = item['alternate_url']
                salary = self.get_salary(item['salary'])
                description = item['snippet']['responsibility']
                id = item['id']
                url_id = 'https://api.hh.ru/vacancies/' + str(id)
                response_id = requests.get(url_id, headers=self.headers).json()
                tags_dict = {'remote': item['schedule']['name'],
                             'experience': response_id['experience']['name']}
                tag = self.get_tag(tags_dict)
                self.res += [f'{title} / {tag} / {salary} / {description} / {link}']
        return self.res



# headers = {
#     'accept': '*/*',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
#                   ' Chrome/105.0.0.0 Safari/537.36'
# }
#
# def get_tag(dict_tags):
#     tags = []
#     if dict_tags['remote'] == 'Удаленная работа':
#         tags.append('Удаленная работа')
#     if dict_tags['experience'] == 'Нет опыта':
#         tags.append('Опыт не нужен')
#     if not tags:
#         return None
#     return ' '.join(tags)
#
#
# def get_salary(salary_dict):
#     if salary_dict is None:
#         return 'По договоренности'
#     if salary_dict['currency'] == 'RUR':
#         rate = 1
#     else:
#         rate = 60
#     if salary_dict['from'] and salary_dict['to']:
#         return f'{salary_dict["from"] * rate} - {salary_dict["to"] * rate} руб'
#     if not salary_dict['to']:
#         return f'от {salary_dict["from"] * rate} руб'
#     return f'до {salary_dict["to"] * rate} руб'
#
#
# res = []
# url = 'https://api.hh.ru/vacancies'
# for i in range(1, 5):
#     par = {"text": "python", 'area': '113', 'per_page': '10', 'page': str(i)}
#     response = requests.get(url, params=par, headers=headers).json()
#     for item in response['items']:
#         title = item['name']
#         link = item['alternate_url']
#         salary = get_salary(item['salary'])
#         description = item['snippet']['responsibility']
#         id = item['id']
#         url_id = 'https://api.hh.ru/vacancies/' + str(id)
#         response_id = requests.get(url_id, headers=headers).json()
#         tags_dict = {'remote': item['schedule']['name'],
#                      'experience': response_id['experience']['name']}
#         tag = get_tag(tags_dict)
#         res += [f'{title} / {tag} / {salary} / {description} / {link}']
#         print(title, link, salary, description, tag, sep='\n')
#
# print(len(res))
# with open('vacancies.txt', 'a', encoding='utf-8') as file:
#     file.write('\n'.join(res))


# class Asd:
#     def get_req(self):
#         url = 'https://yand.ru/'
#         req = rq.get(url)
#         return req.text
#
#
# a = Asd()
#
# try:
#     print(a.get_req())
# except Exception as err:
#     print(f'Сайт не отвечает, {err}')



# page = 1
# vacancies = '1'
# count = 0
# res = []
# while len(vacancies) > 0:
#     url = f'https://russia.superjob.ru/vacancy/search/?keywords=python&page={page}'
#     req = rq.get(url, headers=headers).text
#     soup = BS(req, 'lxml')
#     vacancies = soup.find_all(class_='_8zbxf f-test-vacancy-item _3HN9U hi8Rr _3E2-y _1k9rz')
#     for vacancy in vacancies:
#         name = vacancy.find(class_="_9fIP1 _249GZ _1jb_5 QLdOc")
#         title = name.text
#         link = 'https://russia.superjob.ru' + name.find('a').get('href')
#         salary = vacancy.find(class_='_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi').text
#         description = vacancy.find(class_='_1Nj4W _249GZ _1jb_5 _1dIgi _3qTky').text
#         tag = vacancy.find(class_='_3gyJS _1nh_W')
#         if tag:
#             tag = tag.text
#         print(title, salary, link, description, tag, sep='\n')
#         vac = f'{title} / {tag} / {salary} / {description} / {link}'
#         res += [vac]
#     page += 1
# print(len(res), page)
#
# with open('vacancies.txt', 'w', encoding='utf-8') as file:
#     file.write('\n'.join(res))

