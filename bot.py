from os import path
import json
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from new_users import SearchNewUsers
from connect_users import start

site_link = 'https://www.linkedin.com'
root = path.dirname(path.abspath(__file__))

browser = webdriver.Chrome(path.join(root, 'drivers/chromedriver'))
browser.get(path.join(site_link, 'login'))

json_file = open(path.join(root, 'config.json'))
file = json.load(json_file)
json_file.close()
email = file['email']
password = file['password']
search_by_words = list(map(lambda w : w.lower(), file["search_by_words"]))

element = browser.find_element_by_id('username')
element.send_keys(email)
element = browser.find_element_by_id('password')
element.send_keys(password)
element.submit()

while 'https://www.linkedin.com/checkpoint/challenge' in browser.current_url:
    input('Please make a bot detection. When you finish enter \\n: ')

try:
    while True:
        users = SearchNewUsers(browser, site_link, search_by_words).start_app()
        start(browser, site_link, users)
except KeyboardInterrupt:
    print('Aplication is finishing.')

browser.close()
