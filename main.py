

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import csv
import os.path
import time
import re

from atom.api import Atom, Str, Value, Property, Float
from bs4 import BeautifulSoup

from settings import settings

base_url = 'http://forexfactory.com/'


class Trade(Atom):

    id = Str()
    symbol = Str()
    direction = Str()
    price = Float()


def driver():
    _ = webdriver.Chrome(ChromeDriverManager().install())
    return _


def dump_source(html, file_name):

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    with open(file_name, 'w') as f:
        f.write(soup.prettify())
    return html

def trader_page_html():
    dr = driver()
    dr.get(settings.trade_explorer_url)
    return dump_source(dr.page_source, 'trader_page_source.html')


def trade_list_url():
    """Not in use.
    """
    soup = BeautifulSoup(trader_page_html(), 'html.parser')

    for a in soup.find_all('a'):
        txt = ''.join(a.findAll(text=True))
        if txt == 'Trade List':
            print(txt)
            href = a.get('href')
            url = f"{base_url}{href}"
            return url

        
def open_trade_list():

    html = trader_page_html()
    soup = BeautifulSoup(html, 'html.parser')

    orders_open = soup.find_all('div', {'class': re.compile(r'explorer_overview_trades--open')})
    print(f"Type of Orders open = {type(orders_open)}. Length of orderOpen={len(orders_open)}")
    # print(f"Open orders = {orders_open}")
    tables = list(orders_open[0].find_all('table', recursive=True))
    #     print(f"BEGIN {i} {table} END{i}")
    dump_source(str(tables[0]), 'open_trades.html')

    trades = list()
    for i, tr in enumerate((tables[0].find_all('tbody', recursive=True))[0].find_all('tr')):
        trade = tr.find_all('span')[0].text
        if trade:
            print(f"TRADE = -{trade}-")
            print(f" * * * BEGIN {i} {tr=} ^ ^ ^ END {i}")
            symbol, direction, price = trade.split()
            trades.append(Trade(symbol=symbol, direction=direction, price=float(price)))

    return trades



if __name__ == '__main__':

    print(open_trade_list())
    
