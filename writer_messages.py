from os import path
from time import sleep
from math import floor
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

class WriterMessages:
    user_counter = 1
    num_to_update = 40
    max_users = 95


    def __init__(self, browser, site_link, message):
        self.browser = browser
        self.site_link = site_link
        self.message = message or 'Hello.'

        self.go_to_network_page()

        while self.user_counter < self.max_users:
            try:
                selector_card_li = 'li.mn-connection-card'
                if self.user_counter > self.num_to_update:
                    for i in range(floor(self.user_counter / (self.num_to_update + 1))):
                        sleep(1)
                        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                        WebDriverWait(self.browser, 10).until(expected_conditions.presence_of_element_located(
                            (By.CSS_SELECTOR, f'{selector_card_li}:nth-child({(i + 1) * self.num_to_update + 1})')
                        ))
                user_selector = f'{selector_card_li}:nth-child({self.user_counter}) a.mn-connection-card__link'
                elem = WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR, user_selector)
                ))
                user_href = BeautifulSoup(self.browser.page_source, 'html.parser').select_one(user_selector).get('href')
                elem.click()
                self.send_message()
                print(f'{self.user_counter}. I was on link {user_href}.')
                self.go_to_network_page()
                self.user_counter += 1
            except TimeoutException:
                print('All contacts readed or some Error.')
                break



    def go_to_network_page(self):
        self.browser.get(path.join(self.site_link, 'mynetwork/invite-connect/connections/'))


    def send_message(self):
        message_btn = 'a.message-anywhere-button.pv-s-profile-actions.pv-s-profile-actions--message.ml2.artdeco-button.artdeco-button--2.artdeco-button--primary'

        try:
            WebDriverWait(self.browser, 5).until(
                expected_conditions.element_to_be_clickable(
                    (By.CSS_SELECTOR, message_btn)
                )
            ).click()
        except TimeoutException:
            print('Button message not found.')
            return
        except ElementClickInterceptedException:
            print('I can\'t Click message.')
            return
        sleep(0.5)
        body = BeautifulSoup(self.browser.page_source.encode('utf-8'), 'html.parser')

        try:
            WebDriverWait(self.browser, 1.5).until_not(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, 'ul.msg-s-message-list-content')
                )
            )
            self.browser.find_element_by_css_selector('div.msg-form__contenteditable').send_keys(self.message)
            WebDriverWait(self.browser, 3).until(expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.msg-form__send-button')
            )).click()
        except TimeoutException:
            print('This user has messages.')

        self.browser.find_element_by_css_selector('section.msg-overlay-bubble-header__controls > button[data-control-name="overlay.close_conversation_window"]').click()
        sleep(0.2)
