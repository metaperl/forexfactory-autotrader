from bs4 import BeautifulSoup

with open('grab2.html') as p:
    html = p.read()

soup = BeautifulSoup(html, 'html.parser')

# print(soup.prettify())

# Find the trade list from the main user page
def find_trade_list():
    for a in soup.find_all('a'):
        # href = a.get('href')
        txt = ''.join(a.findAll(text=True))
        if txt == 'Trade List':
            print(txt)
            href = a.get('href')
            print(href)




    # if href and 'list-ticket' in href:
    #     span = a.contents[1]
    #     print(a)
    #     print(span.contents[0])
    #     symbol, direction, price = span.contents[0].split()
    #     print(f"{symbol}, {direction}, {price}")
        

