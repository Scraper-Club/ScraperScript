import time
import scraper_api as api
from db import *
from parsing import GoogleSearchParser, LinkedInCompanyParser

api.URL = 'http://192.168.2.1:8899/api/v1/'
api.KEY = 'ab06267e7d664d3300eda25b399280ffb6750c43'

SEARCH_URL = "https://www.google.com/search?num=30&safe=off&biw=1366&bih=640&tbs=qdr%3Am&q=email+marketing+site" \
             "%3Alinkedin.com%2Fcompany%2F&oq=email+marketing+site%3Alinkedin.com%2Fcompany%2F"


class State:
    START = 'start'
    UPLOADED_SEARCH_LINK = 'upload_search_link'
    WAITING_FOR_TARGET = 'waiting_for_target'
    DOWNLOADED_TARGET_SCRAPES = 'downloaded_target_scrapes'
    DONE = 'done'


# new logic


current_state = State.START


def set_current_state(state):
    global current_state
    with open('state.dat', 'w') as f:
        f.write(str(state))
        f.close()
    current_state = state


def load_state():
    try:
        with open('state.dat', 'r') as f:
            state = f.read()
            f.close()
            return state
    except:
        set_current_state(State.START)


def upload_search_url():
    try:
        search_url_info = api.upload_target_url(SEARCH_URL)
        save_search_url(search_url_info['id'])
        return True

    except api.ScraperApiException as err:
        print(err.message)
        return False


def parse_search_url_result(parser):
    search_url = get_search_url()
    search_url_id = search_url[0]

    try:
        search_url_info = api.get_url_info(search_url_id)

    except api.ScraperApiException as err:
        print(err.message)
        return None

    if search_url_info['scrap']:
        try:
            search_url_content = api.get_scrap_result(search_url_info['scrap'])

        except api.ScraperApiException as err:
            print(err.message)
            return None

        links = parser.parse(search_url_content)
        delete_search_url()
        return links

    else:
        return None


def upload_target_urls(target_urls):
    for target_url in target_urls:
        try:
            url_info = api.upload_target_url(target_url)
            save_target_url(url_info['id'], target_url)
        except api.ScraperApiException as err:
            print(err.message)
            return False

    return True


def download_target_urls():
    not_scraped_targets = get_not_scraped_target_urls()
    if len(not_scraped_targets) == 0:
        return True
    else:
        for target_url in not_scraped_targets:
            try:
                url_info = api.get_url_info(target_url[0])
            except api.ScraperApiException as err:
                print(err.message)
                continue

            if url_info['scrap']:
                try:
                    content = api.get_scrap_result(url_info['scrap'])
                    update_target_url_result(url_info['id'], content)

                except api.ScraperApiException as err:
                    print(err.message)
                    continue

            else:
                continue

        return False


def parse_target_urls(parser):
    scraped_targets = get_scraped_target_urls()

    for target in scraped_targets:
        content = target[3]
        company = parser.parse(content.decode('utf-8'))
        if company:
            print(company)
            save_company(company['name'], company['location'], company['description'], company['website'],
                         company['employees'])
        else:
            print("Bad url " + str(target[1]))


# For GoogleSearchParser to filter the found urls
linkedin_company_url = 'https://www.linkedin.com/company/'


def main():
    print("current state: " + str(current_state))
    if current_state == State.START:
        print("uploading search URL")
        if upload_search_url():
            print("uploaded")
            set_current_state(State.UPLOADED_SEARCH_LINK)

    if current_state == State.UPLOADED_SEARCH_LINK:
        print("checking search URL status")
        parser = GoogleSearchParser(linkedin_company_url)
        result = parse_search_url_result(parser)
        if result:
            print("parsed search url, got " + str(len(result)) + " links")
            if upload_target_urls(result):
                set_current_state(State.WAITING_FOR_TARGET)
                print("uploaded target urls")
        else:
            print("search URL is not scraped yet")

    if current_state == State.WAITING_FOR_TARGET:
        if download_target_urls():
            print("downloaded target url results")
            set_current_state(State.DOWNLOADED_TARGET_SCRAPES)

    if current_state == State.DOWNLOADED_TARGET_SCRAPES:
        parser = LinkedInCompanyParser()
        print("starting parsing results")
        parse_target_urls(parser)
        set_current_state(State.DONE)

    if current_state == State.DONE:
        print("Done")
        exit(0)


if __name__ == '__main__':
    load_state()

    while True:
        set_current_state(State.DOWNLOADED_TARGET_SCRAPES)
        main()
        time.sleep(10)
