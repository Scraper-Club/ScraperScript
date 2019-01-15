from bs4 import BeautifulSoup

from db import Model, TextField, ModelManager
from parsing import TargetResultParser


class CompanyModel(Model):
    name = TextField()
    location = TextField()
    description = TextField()
    website = TextField()
    employees = TextField()


class CompanyManager(ModelManager):
    model = CompanyModel
    table_name = 'company'


class LinkedInCompanyParser(TargetResultParser):
    class Meta:
        model = CompanyModel
        manager = CompanyManager

    def get_result(self, content):
        company = CompanyModel()

        soup = BeautifulSoup(content, 'html.parser')
        company.name = soup.find('h1', {'class': 'top-card__title'}).text

        about_company = soup.find('div', {'class': 'about__content'}) \
            .find('div', {'class': 'about__primary-content'})

        company.description = about_company.find('p', {'class': 'about__description'}).text
        company.website = about_company.find('a', {'class': 'link-without-visited-state'}).text

        next_location = False
        next_employees = False

        for element in about_company.children:
            if next_employees:
                company.employees = element.text
                next_employees = False

            if next_location:
                company.location = element.text
                next_location = False

            if 'headquarters' in element.text.lower():
                next_location = True
            if 'size' in element.text.lower():
                next_employees = True

        return company
