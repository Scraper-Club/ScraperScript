from bs4 import BeautifulSoup


class BaseParser:
    def parse(self, content):
        raise NotImplementedError


class GoogleSearchParser(BaseParser):
    def __init__(self, links_start=None):
        self.links_start = links_start

    def parse(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        result_elements = soup.find('div', {'id': 'rso'}).find_all('div', {'class': 'srg'})
        links = []
        for element in result_elements:
            for child in element.children:
                try:
                    result_link = child.find('a').get('href')
                    if self.links_start:
                        if result_link.startswith(self.links_start):
                            links.append(result_link)
                    else:
                        links.append(result_link)
                except:
                    continue
        return links


class LinkedInCompanyParser(BaseParser):
    def parse(self, content):
        company = {}

        soup = BeautifulSoup(content, 'html.parser')
        company['name'] = soup.find('h1', {'class': 'top-card__title'}).text

        about_company = soup.find('div', {'class': 'about__content'}) \
            .find('div', {'class': 'about__primary-content'})

        company['description'] = about_company.find('p', {'class': 'about__description'}).text
        company['website'] = about_company.find('a', {'class': 'link-without-visited-state'}).text

        next_location = False
        next_employees = False
        company['location'] = None
        company['employees'] = None

        for element in about_company.children:
            if next_employees:
                company['employees'] = element.text
                next_employees = False

            if next_location:
                company['location'] = element.text
                next_location = False

            if 'headquarters' in element.text.lower():
                next_location = True
            if 'size' in element.text.lower():
                next_employees = True

        return company
