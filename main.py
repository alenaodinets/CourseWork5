import requests
from DBManager import DBManager

LINK = 'https://api.hh.ru/vacancies'

if __name__ == '__main__':
    print('')
    your_password = input('Введи пароль от вашей базы данных: ')
    vacancies_count = 0
    while True:
        db_manager = DBManager(your_password)

        user_option = input("Введите 1, чтобы искать вакансии\n"
                            "Введите 2, чтобы вывести список всех компаний и кол-во вакансий\n"
                            "Введите 3, чтобы вывести список всех вакансий с указанием названия компании\n"
                            "Введите 4, чтобы получить среднюю зп по вакансии\n"
                            "Введите 5, чтобы вывести вакансию с самой высокой зп\n"
                            "Введите 6, чтобы искать вакансию по ключевому слову\n"
                            "Введите 7, чтобы выйти\n"
                            "Ваш ввод: ")

        if user_option == '1':
            keyword = input('Введи ключевое слово для поиска вакансий: ')
            count = int(input('Сколько уникальных вакансий ты хочешь получить? '))

            params = {
                'text': keyword,
                'page': 0,
                'per_page': 1
            }

            vacancies = 0
            page = 0
            while vacancies < count:
                params['page'] = page

                response = requests.get(LINK, params=params)
                if response.status_code == 200:
                    items = response.json().get('items')
                    if items:
                        for vacancy in items:
                            if db_manager.is_vacancy_unique(
                                    vacancy['alternate_url']) is False:
                                db_manager.add_vacancy(vacancy)
                                print(f"Добавлено {vacancy['name']} уникальных вакансий в базу данных")
                                vacancies += 1
                                if vacancies >= count:
                                    break
                    else:
                        break
                else:
                    print('Ошибка при выполнении запроса')
                    break

                page += 1

        elif user_option == '2':
            rows = db_manager.get_companies_and_vacancies_count()
            for row in rows:
                print(row)

        elif user_option == '3':
            rows = db_manager.get_all_vacancies()
            for row in rows:
                print(row)

        elif user_option == '4':
            vacancy = input('Введи название вакансии: ').lower()
            rows = db_manager.get_avg_salary(vacancy)
            for row in rows:
                print(row)

        elif user_option == '5':
            rows = db_manager.get_vacancies_with_higher_salary()
            for row in rows:
                print(row)

        elif user_option == '6':
            vacancy = input('Введи название вакансии: ').lower()
            rows = db_manager.get_vacancies_with_keyword(vacancy)
            for row in rows:
                print(row)

        elif user_option == '7':
            break

        else:
            print("Некорректная опция, попробуй еще раз.")

    db_manager.db_close()
