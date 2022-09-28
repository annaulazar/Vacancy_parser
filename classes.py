import requests as rq
from bs4 import BeautifulSoup as BS
from abc import ABC, abstractmethod


class Engine(ABC):
    @abstractmethod
    def get_request(self, user_key):
        pass


class Superjob(Engine):
    def get_request(self, user_key: str) -> list:
        """
        Функция получает список вакансий с сайта Superjob по ключеому слову
        """
        headers = {
            'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/105.0.0.0 Safari/537.36'
        }
        page = 1
        vacancies = '1'
        res = []
        while len(vacancies) > 0:
            url = f'https://russia.superjob.ru/vacancy/search/?keywords={user_key}&page={page}'
            soup = BS(rq.get(url, headers=headers).text, 'lxml')
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
                res += [f'{title} / {tag} / {salary} / {description} / {link}']
            page += 1
        return res


class Hh(Engine):
    def get_request(self, user_key: str) -> list:
        """
        Функция получает список вакансий с сайта hh.ru по ключеому слову
        """
        pass



headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/105.0.0.0 Safari/537.36'
}
page = 1
vacancies = '1'
count = 0
res = []
while len(vacancies) > 0:
    url = f'https://russia.superjob.ru/vacancy/search/?keywords=python&page={page}'
    req = rq.get(url, headers=headers).text
    soup = BS(req, 'lxml')
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
        print(title, salary, link, description, tag, sep='\n')
        vac = f'{title} / {tag} / {salary} / {description} / {link}'
        res += [vac]
    page += 1
print(len(res), page)

with open('vacancies.txt', 'w', encoding='utf-8') as file:
    file.write('\n'.join(res))

