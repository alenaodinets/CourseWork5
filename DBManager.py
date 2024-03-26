
import psycopg2


class DBManager:
    def __init__(self, your_password):
        self.your_password = your_password
        self.conn = psycopg2.connect(
            host='localhost',
            database='vacancy',
            user='postgres',
            password=f'{your_password}')
        self.cur = self.conn.cursor()

    def is_vacancy_unique(self, link_of_vacancy):
        query = "SELECT link FROM vacancy WHERE link = %s"
        self.cur.execute(query, (link_of_vacancy,))
        vacancies = self.cur.fetchall()
        return bool(vacancies)

    def add_vacancy(self, vacancy):
        query = "INSERT INTO vacancy (vacancy, salary, company, description, link) VALUES (%s, %s, %s, %s, %s)"
        values = (
            vacancy['name'].lower(), vacancy['salary']['from'] if vacancy['salary'] else None,
            vacancy['employer']['name'],
            vacancy['snippet']['responsibility'], vacancy['alternate_url'])
        self.cur.execute(query, values)
        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        query = "SELECT company, COUNT(vacancy) as vacancy_count FROM vacancy GROUP BY company;"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return rows

    def get_all_vacancies(self):
        query = f"SELECT vacancy, company, salary, link FROM vacancy;"
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def get_avg_salary(self, keyword: str):
        query = f"SELECT vacancy, AVG(salary) FROM vacancy WHERE vacancy = '{keyword}' GROUP BY vacancy;"
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def get_vacancies_with_higher_salary(self):
        query = f"SELECT * FROM vacancy WHERE salary = (SELECT MAX(salary) FROM vacancy);"
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword):
        query = f"SELECT * FROM vacancy WHERE vacancy = '{keyword}';"
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def db_close(self):
        self.cur.close()
        self.conn.close()
