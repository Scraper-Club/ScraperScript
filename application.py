import time

from GoogleSearchParser import GoogleSearchParser
from LinkedInCompanyParser import LinkedInCompanyParser
from SQLiteAdapter import SQLiteAdapter
from api import ScraperApi

from engine import LinksScrapingEngine

# TODO remove in release
API_URL = 'http://192.168.2.1:8899/api/v1/'

API_KEY = 'ab06267e7d664d3300eda25b399280ffb6750c43'

SEARCH_URL = "https://www.google.com/search?num=30&safe=off&biw=1366&bih=640&tbs=qdr%3Am&q=email+marketing+site" \
             "%3Alinkedin.com%2Fcompany%2F&oq=email+marketing+site%3Alinkedin.com%2Fcompany%2F"

search_parser = GoogleSearchParser('https://www.linkedin.com/company')
target_parser = LinkedInCompanyParser()

db_adapter = SQLiteAdapter('linkedin.db')

api = ScraperApi(API_KEY)
api.URL = API_URL

engine = LinksScrapingEngine(search_parser, target_parser, db_adapter, api, SEARCH_URL)

while True:
    engine.run()
    time.sleep(10)
