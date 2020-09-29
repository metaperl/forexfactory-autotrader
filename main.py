from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from loguru import logger

import csv
import os.path
import time
import re

from atom.api import Atom, Str, Value, Property, Float
from bs4 import BeautifulSoup

from forexfactory_autotrader import db, mt5
from settings import settings

base_url = 'http://forexfactory.com/'


class Trade(Atom):

    id = Str()
    symbol = Str()
    direction = Str()
    price = Str()


    def __str__(self):
        return f"""Trade
            id={self.id}
            symbol={self.symbol}
            direction={self.direction}
            price={self.price}
"""


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
            href = tr.find('a', recursive=True).get('href')
            print(f"TRADE = -{trade}- HREF={href}")
            print(f" * * * BEGIN {i} {tr=} ^ ^ ^ END {i}")
            symbol, direction, price = trade.split()
            trades.append(Trade(id=href, symbol=symbol, direction=direction, price=price))

    return trades


def trade_status(open_trades):
    ids_of_open_trades = {o.id:o for o in open_trades}
    ids_of_placed_trades = set([row for row, in db.session.query(db.PlacedTrades.id)])

    unplaced_trade_ids = set(ids_of_open_trades.keys()) - ids_of_placed_trades
    closed_trade_ids = ids_of_placed_trades - set(ids_of_open_trades.keys())
    # main.Trade instances
    unplaced_trade_objects = [ids_of_open_trades[u] for u in unplaced_trade_ids]
    # db.PlacedTrade instances
    closed_trade_objects = [db.session.query.get(i) for i in closed_trade_ids]

    return unplaced_trade_objects, closed_trade_objects


def open_new_trades(open_trades):
    unopened_trade_objects, closed_trade_objects = trade_status(open_trades)
    # Open new trades
    for new_trade in unopened_trade_objects:
        logger.debug(f"Unopened trade = {new_trade}. Opening")
        order_ticket = mt5.market_order(new_trade)
        if order_ticket:
            logger.debug(f"Order placed via {order_ticket=}")

    # Close trades no longer open
    for closed_trade in closed_trade_objects:
        logger.debug(f"Closed trade = {closed_trade}. Closing")
        order_ticket = mt5.close_trade(closed_trade)
        if order_ticket:
            logger.debug(f"Order placed via {order_ticket=}")

if __name__ == '__main__':

    _ = open_trade_list()
    logger.debug(f"Open trade list={_}")
    open_new_trades(_)
    
