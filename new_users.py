from os import path
import re
from difflib import SequenceMatcher
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

class SearchNewUsers:
    users = []

    def __init__(self, browser, site_link, search_by_words):
        browser.get(path.join(site_link, 'mynetwork'))
        try:
            WebDriverWait(browser, 20).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'mn-cohort-view--list-item'))
            )
        except Exception:
            print('Error in loading file.')
            browser.close()
        self.browser = browser
        self.search_by_words = search_by_words


    def users_validate(self, user_desc):
        for w in self.search_by_words:
            if SequenceMatcher(None, user_desc, w).quick_ratio() > 0.4:
                return True
        return False


    def connect_users(self, block):
        try:
            list = block.find_all('li', 'discover-entity-card discover-entity-card--default-width ember-view')
            for item in list:
                username = item.find('span', 'discover-person-card__name').get_text()
                username = ' '.join(re.findall(r'[A-z]{2,}', username))

                description = item.find('span', 'discover-person-card__occupation t-14 t-black--light t-normal').get_text()
                description = ' '.join(re.findall(r'[A-z]{2,}', description))
                test_by_desc = description.lower()

                user_href = item.find('a', 'ember-view discover-entity-type-card__link')['href']
                if user_href not in self.users and self.users_validate(user_href):
                    self.users.append({'username': username, 'user_directory': user_href, 'description': description})
        except Exception as e:
            print('Error in reading network.')
            print(e)


    def start_app(self):
        source = BeautifulSoup(self.browser.page_source, 'html.parser').find('div', 'application-outlet')
        blocks = source.find_all('li', 'mn-cohort-view--list-item ember-view', limit=5)
        for block in blocks:
            self.connect_users(block)
        return self.users
