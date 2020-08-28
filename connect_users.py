from os import path
def start(browser, site_link, users):
    for user in users:
        try:
            browser.get(site_link + user['user_directory'])
            browser.find_element_by_css_selector('button.pv-s-profile-actions.pv-s-profile-actions--connect.ml2.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view').click()
            browser.find_element_by_css_selector('button.ml1.artdeco-button.artdeco-button--3.artdeco-button--primary.ember-view').click()
            print(f'Connected: {user["username"]}.')
        except Exception as e:
            print('Error in trying connect.')
            print(e)