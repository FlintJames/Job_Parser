import requests


class HH_api_db:
    """Класс для работы с API hh.ru и заполнение таблиц в базу данных"""

    employers_dict = {'ПАО Ростелеком': '2748',
                      'Ozon': '2180',
                      'ООО БЭГГИНС КОФЕ': '3078011',
                      'Додо Пицца (ООО ДОДО ПИЦЦА САМАРА)': '1552384',
                      'ПАО Совкомбанк': '7944',
                      'Красное & Белое, розничная сеть': '1035394',
                      'Тинькофф': '78638',
                      'ООО Люди Любят': '2660054',
                      'Парфюмерно-косметический супермаркет Золотое Яблоко': '776314',
                      'Газпромбанк': '3388'
                      }

    @staticmethod
    def get_request(employer_id) -> dict:
        """Запрос списка работодателей, при наличии вакансий и заработной платы"""
        params = {
            "page": 1,
            "per_page": 100,
            "employer_id": employer_id,
            "only_with_salary": True,
            "area": 113,
            "only_with_vacancies": True
        }
        return requests.get("https://api.hh.ru/vacancies/", params=params).json()['items']

    def get_vacancies(self):
        """Получение списка работодателей"""
        vacancies_list = []
        for employer in self.employers_dict:
            emp_vacancies = self.get_request(self.employers_dict[employer])
            for vacancy in emp_vacancies:
                if vacancy['salary']['from'] is None:
                    salary = 0
                else:
                    salary = vacancy['salary']['from']
                vacancies_list.append(
                    {'url': vacancy['alternate_url'], 'salary': salary,
                     'vacancy_name': vacancy['name'], 'employer': employer})
        return vacancies_list
