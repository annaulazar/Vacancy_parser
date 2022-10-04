import requests as rq
import requests.exceptions
from bs4 import BeautifulSoup as Bs
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

    @staticmethod
    def _get_salary(salary: str) -> str:
        """
        Функция из переданной строки зарплаты получает строку для единого представления,
        так как приходит в виде 55 000 — 75 000 руб. или от 15 000 руб
        """
        if salary == 'По договорённости':
            return '0 руб'
        salary = salary.split(' ')
        if 'от' in salary or 'до' in salary:
            return ' '.join((salary[0], salary[1] + salary[2], salary[3]))
        if '—' not in salary:
            return ' '.join((salary[0] + salary[1], salary[2]))
        return ' '.join((salary[0] + salary[1], salary[2], salary[3] + salary[4], salary[5]))

    def get_request(self, user_key: str) -> list:
        """
        Функция получает список вакансий с сайта Superjob по ключеому слову user_key
        """
        page = 1
        vacancies = '1'
        while len(vacancies) > 0:
            url = f'https://russia.superjob.ru/vacancy/search/?keywords={user_key}&page={page}'
            soup = Bs(rq.get(url, headers=self.headers).text, 'lxml')
            vacancies = soup.find_all(class_='_8zbxf f-test-vacancy-item _3HN9U hi8Rr _3E2-y _1k9rz')
            for vacancy in vacancies:
                name = vacancy.find(class_="_9fIP1 _249GZ _1jb_5 QLdOc")
                title = name.text
                link = 'https://russia.superjob.ru' + name.find('a').get('href')
                salary = self._get_salary(vacancy.find(class_='_2eYAG _1nqY_ _249GZ _1jb_5 _1dIgi').text)
                description = vacancy.find('span', class_='_1Nj4W _249GZ _1jb_5 _1dIgi _3qTky')
                if description:
                    description = description.text
                else:
                    description = 'Нет описания'
                tag = vacancy.find(class_='_3gyJS _1nh_W')
                if tag:
                    tag = tag.text
                self.res += [f'{title} | {tag} | {salary} | {description} | {link}']
            page += 1
        return self.res


class Hh(Engine):

    def __init__(self, headers: dict) -> None:
        self.headers = headers
        self.name = 'hh.ru'
        self.res = []

    @staticmethod
    def _get_tag(dict_tags: dict) -> Optional[str]:
        """
        Функция из переданного словаря полей вакансии получает дополнительные теги ('Опыт не нужен' или
        'Удаленная работа')
        """
        tags = []
        if dict_tags['remote'] == 'Удаленная работа':
            tags.append('Удаленная работа')
        if dict_tags['experience'] == 'Нет опыта':
            tags.append('Опыт не нужен')
        if not tags:
            return None
        return ' '.join(tags)

    @staticmethod
    def _get_salary(salary_dict: dict) -> str:
        """
        Функция из переданного словаря зарплаты получает строку для единого представления
        """
        if salary_dict is None:
            return '0 руб'
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
        Функция получает список вакансий с сайта hh.ru по ключевому слову
        """
        url = 'https://api.hh.ru/vacancies'
        for i in range(1, 4):
            par = {"text": user_key, 'area': '113', 'per_page': '100', 'page': str(i)}
            response = requests.get(url, params=par, headers=self.headers).json()
            for item in response['items']:
                title = item['name']
                link = item['alternate_url']
                salary = self._get_salary(item['salary'])
                description = item['snippet']['responsibility']
                if description is None:
                    description = 'Нет описания'
                vacancy_id = item['id']
                url_id = 'https://api.hh.ru/vacancies/' + str(vacancy_id)
                response_id = requests.get(url_id, headers=self.headers).json()
                tags_dict = {'remote': item['schedule']['name'],
                             'experience': response_id['experience']['name']}
                tag = self._get_tag(tags_dict)
                self.res += [f'{title} | {tag} | {salary} | {description} | {link}']
        return self.res


# class Vacancy:
#     def __init__(self, vacancy: list):
#         pass
#
#     def __repr__(self):
#         pass
