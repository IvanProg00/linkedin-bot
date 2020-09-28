from os import path
import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from new_users import SearchNewUsers
from connect_users import start_connect
from writer_messages import WriterMessages
from errors_handler import error_handler, error_browser_handler

site_link = 'https://www.linkedin.com'
root = path.dirname(path.abspath(__file__))
num_conn = 10

try:
    json_file = open(path.join(root, 'config.json'), 'r')
    config = json.load(json_file)
    json_file.close()
except FileNotFoundError:
    error_handler('Error, file not found.')
except json.JSONDecodeError:
    error_handler('Error in compilation json.')
if type(config) is not dict:
    error_handler('Error, json file must be dictionary.')
email = config.get('email') or ''
password = config.get('password') or ''
search_by_words = list(map(lambda w : w.lower(), config.get("search_by_words"))) or []
message = config.get('message')
browser = webdriver.Chrome

try:
    browser = browser(path.join(root, 'drivers/chromedriver'))
    browser.get(path.join(site_link, 'login'))

    element = browser.find_element_by_id('username')
    element.send_keys(email)
    element = browser.find_element_by_id('password')
    element.send_keys(password)
    element.submit()

    while path.join(site_link, 'checkpoint/challenge') in browser.current_url:
        input('Please make a bot detection. When you finish enter \\n: ')

    if not browser.current_url.startswith(path.join(site_link, 'feed')):
        error_browser_handler(browser, 'Login or Password is incorrect.')

    try:
        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(
            (By.CSS_SELECTOR, 'header.msg-overlay-bubble-header')
        )).click()
    except TimeoutException:
        print("Button messages not found.")

    for i in range(1, num_conn):
        print(f'Bot starts to find and connect people: {i}.')
        users = SearchNewUsers(browser, site_link, search_by_words).start()
        start_connect(browser, site_link, users)

    print('Bot starts to write messages.')
    WriterMessages(browser, site_link, message)

except KeyboardInterrupt:
    error_handler('Aplication is closing...')
except WebDriverException:
    error_browser_handler(browser, 'Browser closed.')

print('Bot has finished his work.')
browser.close()
