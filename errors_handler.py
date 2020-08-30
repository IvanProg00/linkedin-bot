import sys

def error_handler(error_mess = 'Error.'):
    print(error_mess)
    sys.exit()


def error_browser_handler(browser, error_mess = 'Error.'):
    print(error_mess)
    browser.close()
    sys.exit()