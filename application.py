import time

from GoogleSearchParser import GoogleSearchParser
from LinkedInCompanyParser import LinkedInCompanyParser
from SQLiteAdapter import SQLiteAdapter
from api import ScraperApi

from engine import LinksScrapingEngine

API_KEY = 'd20d78a3081878604a724eddb06073c1aa893fed'

SEARCH_URL = "https://www.google.com/search?num=30&safe=off&biw=1366&bih=640&tbs=qdr%3Am&q=email+marketing+site" \
             "%3Alinkedin.com%2Fcompany%2F&oq=email+marketing+site%3Alinkedin.com%2Fcompany%2F"

search_parser = GoogleSearchParser('https://www.linkedin.com/company')
target_parser = LinkedInCompanyParser()

db_adapter = SQLiteAdapter('linkedin.db')

api = ScraperApi(API_KEY)

engine = LinksScrapingEngine(search_parser, target_parser, db_adapter, api, SEARCH_URL)

while True:
    engine.run()
    time.sleep(10)
