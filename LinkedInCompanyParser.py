from bs4 import BeautifulSoup

from db import Model, TextField, ModelManager
from parsing import TargetResultParser, ParserException


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
        good_result = False
        company = CompanyModel()
        soup = BeautifulSoup(content, 'html.parser')

        try:
            company.name = soup.find('h1', {'class': 'top-card__title'}).text
        except:
            print('Failed to get company name')
        else:
            good_result = True

        try:
            about_company = soup.find('div', {'class': 'about__content'}) \
                .find('div', {'class': 'about__primary-content'})
        except:
            raise ParserException(Exception('Bad result'))

        try:
            company.description = about_company.find('p', {'class': 'about__description'}).text
        except:
            pass
        else:
            good_result = True

        try:
            company.website = about_company.find('a', {'class': 'link-without-visited-state'}).text
        except:
            pass
        else:
            good_result = True

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

        if good_result:
            return company
        else:
            raise ParserException(Exception('Bad result'))
