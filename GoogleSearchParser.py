from bs4 import BeautifulSoup
from parsing import SearchResultParser, ParserException


class GoogleSearchParser(SearchResultParser):
    def __init__(self, links_start=None):
        self.links_start = links_start

    def get_links(self, content):
        try:
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

        except Exception as e:
            raise ParserException(e)

        else:
            return links

