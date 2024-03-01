from random import randint
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
from services.scrapping import scrapping_html_to_json

WEBDRIVER_PATH = 'webdriver/chromedriver-win64/chromedriver.exe'

USER_AGENT = {0: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
              1: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
              2: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
              3: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
              4: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
              5: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
              6: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
              }

def parsing_kinopoisk(page: int = 1) -> None:
    serv = Service(os.path.join(os.getcwd(), os.path.normpath(WEBDRIVER_PATH)))

    chrome_options = Options()
    chrome_options.add_argument(f'--user-agent={USER_AGENT[randint(0,6)]}')

    browser = webdriver.Chrome(
        service=serv,
        options=chrome_options
    )
    try:
        browser.get('https://www.kinopoisk.ru/lists/movies/top250/?page={page}'.format(page=page))
        time.sleep(10)
    except Exception as ex:
        print(ex)
    soup = BeautifulSoup(browser.page_source, 'lxml')

    result = scrapping_html_to_json(soup)
    
    return result