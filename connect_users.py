from os import path
from selenium.common.exceptions import NoSuchElementException


def start_connect(browser, site_link, users):
    for user in users:
        try:
            browser.get(site_link + user['user_directory'])
            elem = browser.find_element_by_css_selector('button.pv-s-profile-actions.pv-s-profile-actions--connect.ml2.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view')
            if elem:
                elem.click()

                browser.find_element_by_css_selector('button.ml1.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view').click()
                print(f'Connected: {user["username"]}.')
            else:
                print(f'I can\'t connect {user["username"]}.')
        except NoSuchElementException:
            print(f'I can\'t connect {user["username"]}.')