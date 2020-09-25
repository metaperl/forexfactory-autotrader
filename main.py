

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import csv
import os.path
import time

from atom.api import Atom, Str, Value, Property
from bs4 import BeautifulSoup

from settings import settings

base_url = 'http://forexfactory.com/'

def driver():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver

def trader_page_html():
    dr = driver()

    url = f"{base_url}{settings.trader}"

    dr.get(url)
    s = dr.page_source
    with open('trader_page_source.html', 'w') as f:
        f.write(s)
    return s

def trade_list_url():
    soup = BeautifulSoup(trader_page_html(), 'html.parser')

    for a in soup.find_all('a'):
        txt = ''.join(a.findAll(text=True))
        if txt == 'Trade List':
            print(txt)
            href = a.get('href')
            url = f"{base_url}{href}"
            return url

def open_trade_list():
    dr = driver()
    dr.get(trade_list_url())
    s = dr.page_source
    with open('trade_list_source.html', 'w') as f:
        f.write(s)
    return s
    


if __name__ == '__main__':

    print(open_trade_list())
    
