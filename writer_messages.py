from os import path
from time import sleep
from math import floor
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class WriterMessages:
    users_watched = []
    user_counter = 1
    num_to_update = 40


    def __init__(self, browser, site_link, message):
        self.browser = browser
        self.site_link = site_link
        self.message = message or 'Hello.'

        self.go_to_network_page()

        while self.user_counter < 95:
            if self.user_counter > self.num_to_update:
                for i in range(floor(self.user_counter / (self.num_to_update + 1))):
                    self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    sleep(3)
            user_selector = f'li.mn-connection-card:nth-child({self.user_counter}) a.mn-connection-card__link'
            try:
                user_href = BeautifulSoup(self.browser.page_source, 'html.parser').select_one(user_selector).get('href')
                self.browser.find_element_by_css_selector(user_selector).click()
                self.users_watched.append(user_href)
                self.send_message()
                print(f'{self.user_counter}. I was on link {user_href}.')
                self.go_to_network_page()
                self.user_counter += 1
            except AttributeError:
                print('All contacts readed or some Error.')
                break

        print(self.users_watched)


    def go_to_network_page(self):
        self.browser.get(path.join(self.site_link, 'mynetwork/invite-connect/connections/'))


    def send_message(self):
        message_btn = 'a.message-anywhere-button.pv-s-profile-actions.pv-s-profile-actions--message.ml2.artdeco-button.artdeco-button--2.artdeco-button--primary'

        try:
            WebDriverWait(self.browser, 5).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, message_btn)
                )
            )
            sleep(0.3)
            self.browser.find_element_by_css_selector(message_btn).click()
        except TimeoutException:
            print('Button message not found.')
            return
        except ElementClickInterceptedException:
            print('I can\'t Click message.')
            return
        sleep(0.3)
        body = BeautifulSoup(self.browser.page_source.encode('utf-8'), 'html.parser')
        if body.select_one('ul.msg-s-message-list-content'):
            print('This user has messages.')
        else:
            self.browser.find_element_by_css_selector('div.msg-form__contenteditable').send_keys(self.message)
            sleep(0.3)
            self.browser.find_element_by_css_selector('button.msg-form__send-button').click()
        self.browser.find_element_by_css_selector('section.msg-overlay-bubble-header__controls > button[data-control-name="overlay.close_conversation_window"]').click()
