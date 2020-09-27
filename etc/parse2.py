from bs4 import BeautifulSoup
import re


with open('trade_list_source.html') as p:
    html = p.read()

soup = BeautifulSoup(html, 'html.parser')


div = soup.find_all('div', {'id': re.compile(r'orders_open')})
    print(i)):
    txt = ''.join(table.findAll(text=True))
    if 'Open Trades' in txt:
        print(txt)
        print(table)


