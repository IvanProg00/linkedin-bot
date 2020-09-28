from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.common.by import By


def start_connect(browser, site_link, users):
    for user in users:
        try:
            browser.get(site_link + user['user_directory'])
            WebDriverWait(browser, 4).until(element_to_be_clickable(
                (By.CSS_SELECTOR, 'button.pv-s-profile-actions.pv-s-profile-actions--connect.ml2.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view')
            )).click()
        except TimeoutException:
            print(f'I can\'t connect {user["username"]}.')