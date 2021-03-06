from errors_handler import error_browser_handler
from os import path
from get_info import transform_text
from difflib import SequenceMatcher
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class SearchNewUsers:
    users = []


    def __init__(self, browser, site_link, search_by_words):
        browser.get(path.join(site_link, 'mynetwork'))
        try:
            WebDriverWait(browser, 20).until(
                    expected_conditions.presence_of_element_located(
                        (By.CLASS_NAME, 'mn-cohort-view--list-item')
                    )
                )
        except TimeoutException:
            error_browser_handler(browser, 'Error in loading file.')
        self.browser = browser
        self.search_by_words = search_by_words


    def users_validate(self, user_desc):
        user_words = user_desc.split(' ')
        for w1 in self.search_by_words:
            for w2 in user_words:
                if SequenceMatcher(None, w1, w2).quick_ratio() > 0.65:
                    return True
        return False


    def connect_users(self, block):
        list = block.find_all('li', 'discover-entity-card discover-entity-card--default-width ember-view')
        for item in list:
            username_tag = item.find('span', 'discover-person-card__name')
            if username_tag:
                username = username_tag.get_text()
                username = transform_text(username)

                description = item.find('span', 'discover-person-card__occupation t-14 t-black--light t-normal').get_text()
                description = transform_text(description)
                test_by_desc = description.lower()

                user_href = item.find('a', 'ember-view discover-entity-type-card__link')['href']
                if user_href not in self.users and self.users_validate(test_by_desc):
                    self.users.append({'username': username, 'user_directory': user_href, 'description': description})
            else:
                print('Block don\'t found.')
                break


    def start(self):
        source = BeautifulSoup(self.browser.page_source, 'html.parser').find('div', 'application-outlet')
        blocks = source.find_all('li', 'mn-cohort-view--list-item ember-view', limit=10)
        for block in blocks:
            self.connect_users(block)
        return self.users
